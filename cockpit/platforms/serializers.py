from django.core import serializers
import json

from .models import Instance,AwsEc2Details,Default_config,Project_details

def update_instance_details(instance_details):
    try:
        if len(instance_details) != 0:
            Instance.objects.filter(instance_id=instance_details["instance_id"]).update(**instance_details)
    except Exception as e:
        print("Error updating instance details \n{}".format(e))

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
        print("Error creating instance details in DB \n{}".format(e))


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
                    "guacamole_sharing_url",
                    "user_name",
                    "user_email",
                    "platform_dns_record"
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
        print("Exception--> {}".format(e))
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
                if aws_ec2_details_obj["fields"]["platform"] == platform :
                    temp_dict_obj=aws_ec2_details_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        print("Error in getting aws_ec2_details \n".format(e))
        return {}

def get_default_config(version):
    try:
        data = json.loads(serializers.serialize('json', Default_config.objects.filter(
            version=version),
            fields=(
                    "platform",
                    "version",
                    "framework",
                   # "S3_url",
                )
            )
        )
        if len(data) !=0:
            for default_config_obj in data:
                if default_config_obj["fields"]["version"] == version :
                    temp_dict_obj=default_config_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        print("Error in getting default_congif \n".format(e))
        return {}

def create_project_details(project_details):
    try:
        project_details.objects.create(            
            git_url = project_details['git_url'],
            langauge = project_details['langauge'],
            version = project_details['version'],
            framework = project_details['framework'],
            git_user = project_details['git_user'],
            git_token= project_details['git_token'],
            git_branch = project_details['git_branch'],
            )
    except Exception as e:
        print("Error creating project details in DB \n{}".format(e))

def get_project_details(git_url=None):
    try:
        data = json.loads(serializers.serialize('json', Project_details.objects.filter(
            parameter_value=git_url),
            fields=(
                    "git_url",
                    "langauge",
                    "version",
                    "framework",
                    "git_user",
                    "git_token",
                    "git_branch",
                )
            )
        )
        if len(data) !=0:
            for default_config_obj in data:
                if default_config_obj["fields"]["parameter_value"] == git_url :
                    temp_dict_obj=default_config_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        print("Error in getting project details config \n".format(e))
        return {}

def update_project_details(project_details):
    try:
        if len(project_details) != 0:
            Project_details.objects.filter(git_url=project_details["git_url"]).update(**project_details)
    except Exception as e:
        print("Error updating project details \n{}".format(e))



