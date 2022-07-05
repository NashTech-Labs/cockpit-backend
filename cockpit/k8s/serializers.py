from django.core import serializers
import json
from .models import KubernetesConfig

def create_kubernetes_config_entry_in_db(cluster_details):
    try:
        KubernetesConfig.objects.create(            
            bearer_token=cluster_details["bearer_token"],
            version=cluster_details["version"],
            cluster_name=cluster_details["cluster_name"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            kubeconfig =cluster_details["kubeconfig"],
            cloud=cluster_details["cloud"]
            )
    except Exception as e:
        print("Error creating cluster details in DB \n{}".format(e))

def list_imported_cluster():
    try:
        data = list(KubernetesConfig.objects.all().values('id','cluster_name','version','api_server_endpoint'))
        if len(data) != 0:
            return {"clusters":data,"message":"SUCCESFUL"}
        else:
            return {"clusters":[],"message":"NO CLUSTERS FOUND"}
    except Exception as e:
        print("Exception--> {}".format(e))
        return {"clusters":[], "message":"NO CLUSTERS FOUND"}

def get_cluster_details(cluster_name=None):
    """returns instnace details based on cluster_ip if it exits in db 
    else return None 
    """
    try:
        data = json.loads(serializers.serialize('json', KubernetesConfig.objects.filter(
            cluster_name=cluster_name),
            fields=(
                "bearer_token",
                "version",
                "cluster_name",
                "api_server_endpoint",
                "kubeconfig",
                "cloud"
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