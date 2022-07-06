from kubernetes import client
from kubernetes.client import ApiClient
import json
from kubernetes.client.rest import ApiException

import logging

#Get an instance of a specific named logger
logger = logging.getLogger('k8s-view')

def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
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

def __format_data_for_service(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for service in json_data["items"]:
                temp_dict={
                    "service": service["metadata"]["name"],
                    "namespace": service["metadata"]["namespace"],
                }
                temp_list.append(temp_dict)
        return temp_list

def __format_data_for_create_service(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list

def get_services(cluster_details,namespace="default",all_namespaces=True):    
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            service_list =client_api.list_service_for_all_namespaces(watch=False)
            data=__format_data_for_service(service_list) 
            #print("Deployment Set under all namespaces: {}".format(data))    
            return data
        else:
            service_list = client_api.list_namespaced_service(namespace)
            data=__format_data_for_service(service_list) 
            #print("DeploySet under namespaces {}: {}".format(namespace,data))            
            return data

def create_service(cluster_details,yaml_body=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.create_namespaced_service(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_service(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_service:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_service(e.body)

def delete_service(cluster_details,k8s_object_name, namespace="default"):
   
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )

        resp = client_api.delete_namespaced_service(
            name=k8s_object_name,
            namespace="{}".format(namespace),
            body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=5
            ),
        )
        data=__format_data_for_create_service(resp)
        return data
    except ApiException as e:
        print("ERROR IN delete_service:\n{}".format(e.body))
        return __format_data_for_create_service(e.body)

def update_service(cluster_details,k8s_object_name=None,yaml_body=None,namespace="default"):
    # Delete deployment
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )

        resp = client_api.patch_namespaced_service(
            name=k8s_object_name,
            namespace="{}".format(namespace),
            body=yaml_body
        )
        data=__format_data_for_create_service(resp)
        return data
    except ApiException as e:
        print("ERROR IN update_service:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_service(e.body)