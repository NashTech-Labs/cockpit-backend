from kubernetes import client
from kubernetes.client import ApiClient


def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
        #corev1api=("configmap","node","config_map","secret","service","namespace","resource")
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

def __format_data_for_configmap(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for configmap in json_data["items"]:
                temp_dict={
                    "configmap": configmap["metadata"]["name"],
                    "namespace": configmap["metadata"]["namespace"]
                }
                temp_list.append(temp_dict)
        return temp_list
    

def get_configmaps(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            configmap_list =client_api.list_config_map_for_all_namespaces(watch=False)
            data=__format_data_for_configmap(configmap_list)
            #print("configmaps under all namespaces: {}".format(data))
            return data
        else:
            configmap_list = client_api.list_namespaced_config_map(namespace)
            data=__format_data_for_configmap(configmap_list)
            #print("configmaps under namespaces {}: {}".format(namespace,data))
            return data