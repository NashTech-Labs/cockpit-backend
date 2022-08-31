import json
from kubernetes import client
from kubernetes.client import ApiClient
import yaml
from os import path
from kubernetes.client.rest import ApiException

def __get_kubernetes_networkv1client(bearer_token,api_server_endpoint):
    try:
        #corev1api=("pod","node","config_map","secret","service","namespace","resource")
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.NetworkingV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_ingress(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for ingress in json_data["items"]:
                temp_dict={
                    "ingress": ingress["metadata"]["name"],
                    "namespace": ingress["metadata"]["namespace"],
                    
                }
                temp_list.append(temp_dict)
        return temp_list
def __format_data_for_create_ingress(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list
def get_ingress(cluster_details,namespace="default",all_namespaces=False):

    client_api= __get_kubernetes_networkv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    if all_namespaces is True:
        ingress_list =client_api.list_ingress_for_all_namespaces()
        data=__format_data_for_ingress(ingress_list)
        # print("Ingress under all namespaces: {}".format(data))
        return data
    else:
        ingress_list = client_api.list_namespaced_ingress(namespace)
        data=__format_data_for_ingress(ingress_list)
        # print("ingress under namespaces {}: {}".format(namespace,data))
        return data
def create_ingress(cluster_details,yaml_body=None,namespace="default"):
 
    try:
        client_api= __get_kubernetes_networkv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        resp=client_api.create_namespaced_ingress(
            body=yaml_body, namespace="{}".format(namespace))
        data=__format_data_for_create_ingress(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_ingress(e.body)
def update_ingress(cluster_details,k8s_object_name=None,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_networkv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp=client_api.patch_namespaced_ingress(
            name=k8s_object_name,body=yaml_body, namespace="{}".format(namespace))
        data=__format_data_for_create_ingress(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_ingress(e.body)
def delete_ingress(cluster_details,k8s_object_name=None,namespace="default"):
    try:
        client_api= __get_kubernetes_networkv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        
        resp=client_api.delete_namespaced_ingress(
            name=k8s_object_name,
            namespace="{}".format(namespace),
            body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        ))
        data=__format_data_for_create_ingress(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_ingress(e.body)