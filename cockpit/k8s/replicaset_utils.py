from kubernetes import client
from kubernetes.client import ApiClient
import json
from kubernetes.client.rest import ApiException

def __get_kubernetes_appsv1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.AppsV1Api()                                 #Changes
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_replicaset(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for replicaset in json_data["items"]:
                temp_dict={
                    "replicaset": replicaset["metadata"]["name"],
                    "namespace": replicaset["metadata"]["namespace"]
                }
                temp_list.append(temp_dict)
        return temp_list

def __format_data_for_create_replicaset(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list

def get_replicasets(cluster_details,namespace="default",all_namespaces=True):                              #changes
        client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            replicaset_list =client_api.list_replica_set_for_all_namespaces(watch=False)
            data=__format_data_for_replicaset(replicaset_list)
            #print("Replica Set under all namespaces: {}".format(data))                    
            return data
        else:
            replicaset_list = client_api.list_namespaced_replica_set(namespace)
            data=__format_data_for_replicaset(replicaset_list)
            #print("Replica Set under namespaces {}: {}".format(namespace,data))                      #changes
            return data

def create_replicaset(cluster_details,yaml_body=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_appsv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.create_namespaced_replica_set(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_replicaset(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_replicaset(e.body)