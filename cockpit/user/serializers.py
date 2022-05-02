from django.core import serializers
import json

from .models import User


def create_user_entry_in_db(user_details):
    try:
        User.objects.create(            
            user_email=user_details['user_email'],
            user_name = user_details['user_name'],
            )
    except Exception as e:
        print("Error creating user details in DB \n{}".format(e))
