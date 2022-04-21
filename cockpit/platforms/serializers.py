from django.core import serializers
import json

from .models import Instance

def update_instance_details(instance_details):
    try:
        pass
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
            platform_state= instance_details['platform_state']
            )
    except Exception as e:
        print("Error creating instance details in DB \n{}".format(e))