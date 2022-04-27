from django.core import serializers
import json
from .models import Instance,AwsEc2Details
import logging

logger=logging.getLogger("platforms")


def update_instance_details(instance_details):
    try:
        if len(instance_details) != 0:
            Instance.objects.filter(instance_id=instance_details["instance_id"]).update(**instance_details)
    except Exception as e:
        logger.error("Error updating instance details \n{}".format(e))

def create_ec2_entry_in_db(instance_details):
    try:
        Instance.objects.create(            
            instance_id = instance_details['instance_id'],
            public_ip = instance_details['public_ip'],
            private_ip = instance_details['private_ip'],
            instance_state = instance_details['instance_state'],
            platform = instance_details['platform'],
            platform_state= instance_details['platform_state'],
            user_name = instance_details['user_name'],
            user_password = instance_details['user_password']
            )
    except Exception as e:
        logger.error("Error creating instance details in DB \n{}".format(e))


def get_instance_details(instance_id=None):
    """returns instnace details based on instance_ip if it exits in db 
    else return None 
    """
    try:
        data = json.loads(serializers.serialize('json', Instance.objects.filter(
            instance_id=instance_id),
            fields=(
                    "platform_id",
                    "instance_id", 
                    "public_ip" ,
                    "private_ip",
                    "instance_state" ,
                    "platform" ,
                    "platform_state",
                    "guacamole_ws_url",
                    "guacamole_sharing_url" 
                )
            )
        )
        if len(data) !=0:
            for instance_obj in data:

                if instance_obj["fields"]["instance_id"] == instance_id :
                    temp_dict_obj=instance_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        logger.error("Exception--> {}".format(e))
        return {}


def get_aws_ec2_details(platform):
    try:
        data = json.loads(serializers.serialize('json', AwsEc2Details.objects.filter(
            platform=platform),
            fields=(
                    "image_id",
                    "instance_type",
                    "subnet_id",
                    "security_group_ids",
                    "iam_profile",
                    "key_name",
                    "platform"
                )
            )
        )
        if len(data) !=0:
            for aws_ec2_details_obj in data:

                if aws_ec2_details_obj["fields"]["instance_id"] == platform :
                    temp_dict_obj=aws_ec2_details_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        logger.error("Error in getting aws_ec2_details \n".format(e))
        return {}