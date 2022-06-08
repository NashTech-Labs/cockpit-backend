import json
from kubernetes import client, config
from kubernetes.client import ApiClient


def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
        #corev1api=("pod","node","config_map","secret","service","namespace","resource")
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

def __format_data_for_pod(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for pod in json_data["items"]:
                temp_dict={
                    "pod": pod["metadata"]["name"],
                    "namespace": pod["metadata"]["namespace"],
                    "status": pod["status"]["phase"]
                }
                temp_list.append(temp_dict)
        return temp_list
    

def get_pods(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            pod_list =client_api.list_pod_for_all_namespaces(watch=False)
            data=__format_data_for_pod(pod_list)
            #print("Pods under all namespaces: {}".format(data))
            return data
        else:
            pod_list = client_api.list_namespaced_pod(namespace)
            data=__format_data_for_pod(pod_list)
            #print("Pods under namespaces {}: {}".format(namespace,data))
            return data