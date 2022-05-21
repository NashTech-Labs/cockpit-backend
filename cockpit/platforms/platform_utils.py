from .aws_utils import *
from .serializers import *
from .platform_state import *
from .mail import *

from cockpit.celery import app 
from guacamole.guacamole_utils import *


@app.task(time_limit=600,queue='default')
def create_platform(platform_details):
    """Create a Requested Platform
    arg: 
    {
        "user_name":"sachinvd",
        "user_email":"sachinvd@gmail.com",
        "platform":"jenkins"
    }
    """
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
                URL,WS=paltform_guacamole(connection_data)
                platform_dns_record=create_route53_a_record(
                    instance_data['public_ip'],
                    instance_data['platform']
                    )
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
