from django.core import serializers
import json
from .models import ArgocdConfig

def create_argocd_config_entry_in_db(cluster_details):
    try:
        ArgocdConfig.objects.create(
            bearer_token=cluster_details["bearer_token"],
            git_url=cluster_details["git_url"],
            username=cluster_details["username"],
            password=cluster_details["password"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            cluster_name=cluster_details["cluster_name"]
        )
    except Exception as e:
        print("Error creating cluster details in DB \n{}".format(e))

def get_application_details(cluster_name=None):
    """returns application details based on server_endpoint if it exits in db 
    else return None 
    """
    try:
        data = json.loads(serializers.serialize('json', ArgocdConfig.objects.filter(
            cluster_name=cluster_name),
            fields=(
                "bearer_token",
                "git_url",
                "username",
                "password",
                "api_server_endpoint",
                "cluster_name"
                )
            )
        )
        if len(data) !=0:
            for cluster_obj in data:

                if cluster_obj["fields"]["cluster_name"] == cluster_name :
                    temp_dict_obj=cluster_obj["fields"]
                    return  temp_dict_obj
        return {}
    except Exception as e:
        print("Exception--> {}".format(e))
        return {}