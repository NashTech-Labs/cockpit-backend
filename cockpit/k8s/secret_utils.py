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
    
# Get Function For Secrets


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


# Create Function for Secrets

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


# Update Function For Secrets

def update_secret(cluster_details , data , string_data , name):
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

    api = client_api.patch_namespaced_secret(namespace="default", body=secret , name=name)
    return api




#  Delete Function For Secrets 

def delete_secret(cluster_details , name):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    #api1 = client_api.patch_namespaced_config_map(name=name , namespace="default", body={})
    api = client_api.delete_namespaced_secret(name=name , namespace="default", body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5))
    return api

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlpQYVBWbm5Kb1FMN0NFMzR3MnlSbXE1R3hlQ3RfTDVQZWNBQmVmSUpNMFEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1jbHVzdGVyLXJvbGUtdG9rZW4tdnJtamsiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWNsdXN0ZXItcm9sZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjcwZGVlYjU1LWVmNDItNGQxNC05NjM3LThkYWFlZGU4NzYwNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRhc2hib2FyZC1jbHVzdGVyLXJvbGUifQ.kilBAHfo2iRdlILhZPFn0XDfSwz3rHSM15h46B9g4wgzt7EJWkvc1GwVhpmcPNmd4Kj_ePcWILJKtjZTQDknkjyNFzD2NeX3v92-LfEA1C5svljwBXFY3S4AUZCfWFhpYEV-qYGsTKqVgeWqGFpy9r8Sd4qkR_zecvAUdF_bRkDJZ7_JDp6BCqvoi_KDmyWxpeDEe6ueYa0KLAHdJMKcH3fmN4h9WnBuuEBg2Q0gEetxdui0cWbRWQQplhR7lP_-V364NmgJByesuT69VSL2CY_DGxb8XU4oFnChlNsHd_Qt3GMRUGrW3DxtHZrdtv34REBV_tR5UqtnVLQCAQpQJA"
API = "https://34.69.172.158"
cluster = {
    "bearer_token" : TOKEN,
    "api_server_endpoint" : API
}
cm={
    "name": "abcd"
}
delete_secret(cluster , "deekasha-01")

