from pydoc import cli
import boto3
import os,time
import json
from .serializers import create_ec2_entry_in_db
import logging
import secrets

def __create_random_password():
    return secrets.token_urlsafe(10)
 
def create_aws_client(client=None):
    try:
        if client is not None:
            client=boto3.client('{}'.format(client))
            return client
        else:
            return None
    except Exception as e:
        print("Error in creating ec2 client \n{}".format(e))
        return None

def json_format_instance(public_ip=None,
                        private_ip=None,
                        instance_state=None,
                        platform=None,
                        instance_id=None,
                        platform_state=1401

                        ):
    instance={
        'public_ip': "{}".format(public_ip if public_ip is not None else 'None'),
        'private_ip': "{}".format(private_ip if private_ip is not None else 'None'),
        'instance_state': "{}".format(instance_state if instance_state is not None else 'None'),
        'instance_id':'{}'.format(instance_id if instance_id is not None else 'None'),
        'platform':'{}'.format(platform if platform is not None else 'None'),
        'platform_state': '{}'.format(platform_state if platform_state is not None else 'None')
    }
    return instance

def bash_script_create_user(user_name=None,user_password=None):
    try:
        if user_name is not None and user_password is not None:
            user_creation_template="""#!bin/bash
            echo "Creating user {0}" &>> /var/log/cockpit_user.log
            sudo useradd -m {0} -s /bin/bash &>> /var/log/cockpit_user.log
            echo "{0}:{1}" | chpasswd  &>> /var/log/cockpit_user.log
            """.format(user_name,user_password)
            return user_creation_template
        else:
            return None
    except Exception as e:
        print("Error in bash_script_create_user \n{}".format(e))
        return None

def base64_userdata(data):
    try:
        return data
    except Exception as e:
        print("Error in creating base64_userdata \n{}".format(e))
        return None

def create_ec2_instance(instance_details):
    """
        instance_details = {
            'image_id':"",
            "key_name":"",
            'iam_profile':'',
            'subnet_id':'',
            'instance_type':'',
            'security_group_id':'',
            'platform': '',
            'user_name' '',
            'email':''
        }
    """
    user_password=__create_random_password()
    try:
        print("Launching the ec2 instance")

        ec2_client=create_aws_client(client='ec2')
        if ec2_client is not None:
            instances = ec2_client.run_instances(
                ImageId=instance_details["image_id"], 
                KeyName=instance_details["key_name"],
                MinCount=1, 
                MaxCount=1,
                InstanceType=instance_details["instance_type"],
                SubnetId=instance_details["subnet_id"],
                SecurityGroupIds=["{}".format(instance_details["security_group_ids"])],
                UserData='{}'.format(bash_script_create_user(
                    user_name=instance_details['user_name'],
                    user_password=user_password)
                    ),
                BlockDeviceMappings=[
                    {
                        'DeviceName': '/dev/sdh',
                        'Ebs': {
                            'VolumeSize': 30,
                        },
                    },
                ],
                IamInstanceProfile={
                    'Arn': instance_details["iam_profile"]
                },
                TagSpecifications = [
                        {
                            'ResourceType': "instance",
                            'Tags':[
                                {
                                    "Key":"Platform",
                                    "Value" : instance_details["platform"]

                                },
                                {
                                    "Key":"Name",
                                    "Value" : "{0}-{1}".format(
                                        instance_details["platform"],
                                        instance_details['user_name']
                                        )

                                },                        
                            ]
                        }
                ],
            )
            
            print("response:{}".format(instances))
            PrivateIpAddress=instances["Instances"][0]["NetworkInterfaces"][0]['PrivateIpAddress']
            InstanceId = str(instances["Instances"][0]["InstanceId"])
            create_ec2_entry_in_db(
                {
                    'instance_id': "{}".format(InstanceId),
                    'private_ip':"{}".format(PrivateIpAddress),
                    'public_ip':"None",
                    'instance_state':"pending",
                    'platform':'{}'.format(instance_details['platform']),
                    'platform_state': 1003,
                    'user_name':"{}".format(instance_details['user_name']),
                    'user_password': "{}".format(user_password)
                }
            )

            describe_instance = ec2_client.describe_instances(InstanceIds=[InstanceId])

            print("Checking for the instance to be in running state...")
            count = 0
            while True:
                count = count +1
                time.sleep(5)
                describe_instance_status = ec2_client.describe_instance_status(InstanceIds=[InstanceId])
                print("describe \n{}".format(describe_instance_status))
                if describe_instance_status["InstanceStatuses"]:
                    
                    instance_code = describe_instance_status["InstanceStatuses"][0]["InstanceState"]["Code"]
                    InstanceStatus = describe_instance_status["InstanceStatuses"][0]["InstanceStatus"]["Status"]
                    SystemStatus = describe_instance_status["InstanceStatuses"][0]["SystemStatus"]["Status"]
                    print("instance_state: {}, {},{}".format(instance_code, InstanceStatus,SystemStatus))
                    if instance_code == 16 and InstanceStatus == "ok" and SystemStatus == "ok" :
                        print(InstanceId + " ec2 instance is up and running successfully ")
                        break
                if count == 10:
                    print("Waited for more than 50 seconds, instance " +InstanceId + " doesnt come up,\
                                    please check in AWS GUI")
                    break
            print("Successfull created the ec2 instance..")
            print("instance Id for your reference : " +InstanceId )
            describe_instance = ec2_client.describe_instances(InstanceIds=[InstanceId])
            InstanceState= str(describe_instance["Reservations"][0]["Instances"][0]['State']['Name'])
            PublicIpAddress = str(describe_instance["Reservations"][0]["Instances"][0]["PublicIpAddress"])
            print("PublicIpAddress for your reference : " +PublicIpAddress )


            return {
                'instance_id':'{}'.format(InstanceId),
                'public_ip':'{}'.format(PublicIpAddress),
                'private_ip':'{}'.format(PrivateIpAddress),
                'instance_state':'{}'.format(InstanceState),
                'platform':'{}'.format(instance_details['platform']),
                'platform_state':1004,
                'user_name': '{}'.format(instance_details['user_name']),
                'user_password':'{}'.format(user_password)
                }
        else:
            return json_format_instance()    
    except Exception as e:
        print("Error in creating ec2 \n{}".format(e))
        return {
            'instance_id':'None',
            'public_ip':'None',
            'private_ip':'None',
            'instance_state':'None',
            'platform':'{}'.format(instance_details['platform']),
            'platform_state': 1401
            }


#instance_details={'image_id':"ami-04505e74c0741db8d","key_name":"mykeypair",'iam_profile':'arn:aws:iam::240360265167:instance-profile/SSMEc2CoreRole','subnet_id':'subnet-00925fb32ec58642b','instance_type':'t2.micro','security_group_ids':['sg-039ab3daa43b8cc52'],'platform':'JENKINS','user_name':'sachinvd','user_email':'something@gmail.com',}