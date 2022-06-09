from kubernetes import client
from kubernetes.client import ApiClient


def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
        #corev1api=("secret","node","config_map","secret","service","namespace","resource")
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.CoreV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_secret(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for secret in json_data["items"]:
                temp_dict={
                    "secret": secret["metadata"]["name"],
                    "namespace": secret["metadata"]["namespace"]
                }
                temp_list.append(temp_dict)
        return temp_list
    

def get_secrets(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            secret_list =client_api.list_secret_for_all_namespaces(watch=False)
            data=__format_data_for_secret(secret_list)
            #print("secrets under all namespaces: {}".format(data))
            return data
        else:
            secret_list = client_api.list_namespaced_secret(namespace)
            data=__format_data_for_secret(secret_list)
            #print("secrets under namespaces {}: {}".format(namespace,data))
            return data


from django.shortcuts import render
import json
from kubernetes import client, config
#from rest_framework.decorators import api_view


def create_secret(cluster_details , data , string_data):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    secret = client.V1Secret(
        api_version="v1",
        kind="Secret",
        metadata=client.V1ObjectMeta(name="deekasha-02"),
        data=data , 
        string_data=string_data
    )

    api = client_api.create_namespaced_secret(namespace="default", body=secret)
    return api


# stringdata={
#     "app": "cockpit"
# }
# data={
#     "app-01": "Y29ja3BpdAo="
# }

#create_secret(cluster_details, data , stringdata)
