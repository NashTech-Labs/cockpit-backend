from django.core import serializers
import json

from .models import User


def create_ec2_entry_in_db(user_details):
    try:
        User.objects.create(            
            email=user_details['email'],
            user_name = user_details['user_name'],
            )
    except Exception as e:
        print("Error creating user details in DB \n{}".format(e))
