from .aws_utils import *
from .serializers import *
from .platform_state import *

from cockpit.celery import app 
from guacamole.guacamole_utils import *
@app.task(queue='default')
def create_platform(platform_details):
    """Create a Requested Platform
    arg: 
    {
        "user_name":"sachinvd",
        "email":"sachinvd@gmail.com",
        "platform":"jenkins"
    }
    """
    try:
        aws_ec2_details=get_aws_ec2_details(platform_details["platform"])
        if len(aws_ec2_details) != 0:
            print("aws_ec2_details :{}".format(aws_ec2_details))
            platform_details.update(aws_ec2_details)
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
                print("connection_data ;{}".format(connection_data))
                URL,WS=paltform_guacamole(connection_data)
                update_instance_details(
                    {
                        "guacamole_sharing_url":"{}".format(URL['URL']),
                        "guacamole_ws_url":'{}'.format(WS),
                        "instance_id" : "{}".format(instance_data["instance_id"]),
                })
                print("URL In PLATFORM SETUP:{}".format(URL))
            else:
                print("NOT ABLE GET INSTANCE INTO RUNNING STATE")
        else:
            print("send message requested platform is not available cuurrently")
            #send message requested platform is not available cuurrently
    except Exception as e:
        print("Error creating platform \n{}".format(e))
        #send message requested platform is not available cuurrently
