from django.core import serializers
import json

from .models import Instance,AwsEc2Details,ProjectDetails

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

def create_project_details_entry_in_db(project_details):
    try:
        ProjectDetails.objects.create(            
            git_url = project_details['project_details']['git_url'],
            git_branch = project_details['project_details']['git_branch'],
            git_token = project_details['project_details']['git_token'],
            docker_reponame = project_details['project_details']['docker_reponame'],
            docker_tag = project_details['project_details']['docker_tag'],
            docker_file_path= project_details['project_details']['docker_file_path'],
            docker_build_context = project_details['project_details']['docker_build_context'],
            docker_username = project_details['project_details']['docker_username'],
            docker_password = project_details['project_details']['docker_password'],
            platform= project_details['platform'],
            language= project_details['project_details']['language'],
            version= project_details['project_details']['version'],
            framework = project_details['project_details']['framework'],
            user_name = project_details['user_name'],
            user_email = project_details['user_email']
            )
    except Exception as e:
        print("Error creating instance details in DB \n{}".format(e))