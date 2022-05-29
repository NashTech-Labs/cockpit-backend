from .aws_utils import *
from .serializers import *
from .platform_state import *
from .mail import *

from cockpit.celery import app 
from guacamole.guacamole_utils import *
from .jenkins_api import *


@app.task(time_limit=600,queue='default')
def create_platform(platform_details):
    """Create a Requested Platform
    arg: 
        {
            "user_name":"sachinvd",
            "user_email":"sachinvd@gmail.com",
            "platform":"jenkins",
            "project_details":{
                "git_url":"",
                "git_branch":"",
                "git_token":"",
                "docker_reponame":"",
                "docker_tag":"",
                "docker_registry_url":"",
                "docker_username":"",
                "docker_password":"",
                "docker_file_path":"",
                "docker_build_context":"",
                "language":"",
                "version":"",
                "framework":""
            }
        }
    """
    project_details=platform_details["project_details"]
    try:
        aws_ec2_details=get_aws_ec2_details(platform_details["platform"])
        if len(aws_ec2_details) != 0:
            print("aws_ec2_details :{}".format(aws_ec2_details))
            platform_details.update(aws_ec2_details)
            print("Platform Details {}".format(platform_details))
            instance_data=create_ec2_instance(platform_details)
            update_instance_details(instance_data)

            if instance_data['instance_state'].lower() == "running":
                connection_data={
                    'name' : '{}'.format(instance_data["instance_id"]),
                    'hostname' : "{}".format(instance_data["public_ip"]),
                    'port' : '22',
                    'protocol' : 'ssh',
                    'username' : '{}'.format(instance_data["user_name"]),
                    'password' : '{}'.format(instance_data["user_password"]),
                    'private-key' : ''
                }


                update_instance_details(
                    {
                    "instance_id" : "{}".format(instance_data["instance_id"]),
                    "platform_state": 1005}

                )

                print("connection_data ;{}".format(connection_data))

                
                platform_dns_record=create_route53_a_record(
                    instance_data['public_ip'],
                    instance_data['platform']
                    )

                jjb_client=JenkinsJobBuilderExecutable(
                    server="http://{}".format(instance_data["public_ip"]),
                    username="{}".format(os.getenv("JENKINS_ADMIN_USER","admin")),
                    password="{}".format(os.getenv("JENKINS_ADMIN_PASSWORD","admin"))
                    )

                response=jjb_client.create_jenkins_user(
                    jusername="{}".format(instance_data["user_name"]),
                    jpassword="{}".format(instance_data["user_password"]),
                    jemail="{}".format(platform_details["user_email"])

                )

                if response == 200:
                    print("jenkins user-setup successfull")
                else:
                    print("jenkins user-setup failed")

                jenkins_git_cred=jjb_client.create_credential(
                    credusername='{}'.format(platform_details["user_name"]),
                    credpassword='{}'.format(project_details["git_token"])
                    )
                jenkins_docker_cred=jjb_client.create_credential(
                    credusername='{}'.format(project_details["docker_username"]),
                    credpassword='{}'.format(project_details["docker_password"])
                    )
                    
                yaml_job_data=create_job_yml(
                        git_url=project_details["git_url"],
                        git_credentials_id=jenkins_git_cred,
                        git_branch=project_details["git_branch"],
                        docker_reponame=project_details["docker_reponame"],
                        docker_tag=project_details["docker_tag"],
                        docker_file_path=project_details["docker_file_path"],
                        docker_build_context=project_details["docker_build_context"]

                        )
                    
                yaml_job_path=create_yaml_file(yaml_job_data,platform_dns_record,file_path=os.getenv("JENKINS_CONFIG","/config"))
                xml_job_path=jjb_client.generate_xml(yaml_job_path,platform_dns_record)
                jjb_client.create_job(xml_job_path,'jjb_job')

                print("XML JOB PATH {0}\n YAML JOB PATH {1}".format(xml_job_path,yaml_job_path))
                
                URL,WS=paltform_guacamole(connection_data)

                update_instance_details(
                    {
                        "guacamole_sharing_url":"{}".format(URL['URL']),
                        "guacamole_ws_url":'{}'.format(WS),
                        "platform_dns_record":'{}'.format(platform_dns_record),
                        "instance_id" : "{}".format(instance_data["instance_id"]),
                        "platform_state": 1006
                })

                print("PLATFORM DNS RECORD: {}".format(platform_dns_record))
                print("URL In PLATFORM SETUP:{}".format(URL))
                details=get_instance_details(instance_id=instance_data['instance_id'])
                send_cockpit_mail(details)
            else:
                print("NOT ABLE GET INSTANCE INTO RUNNING STATE")
                temp={
                    "platform_dns_record":None,
                    "guacamole_sharing_url":None
                }
                platform_details.update(temp)
                send_cockpit_mail(platform_details)
        else:
            print("send message requested platform is not available cuurrently")
            #send message requested platform is not available cuurrently
            temp={
                    "platform_dns_record":None,
                    "guacamole_sharing_url":None
                }
            platform_details.update(temp)
            update_instance_details(
                    {
                    "instance_id" : "{}".format(instance_data["instance_id"]),
                    "platform_state": 1401}

                )
            send_cockpit_mail(platform_details)
    except Exception as e:
        print("Error creating platform \n{}".format(e))
        temp={
            "platform_dns_record":None,
            "guacamole_sharing_url":None
        }
        platform_details.update(temp)
        send_cockpit_mail(platform_details)
        #send message requested platform is not available cuurrently
