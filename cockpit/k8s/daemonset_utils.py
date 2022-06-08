from kubernetes import client
from kubernetes.client import ApiClient

def __get_kubernetes_appsv1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.AppsV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_daemonset(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for daemonset in json_data["items"]:
                temp_dict={
                    "daemonset": daemonset["metadata"]["name"],
                    "namespace": daemonset["metadata"]["namespace"],
                }
                temp_list.append(temp_dict)
        return temp_list

def get_daemonsets(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            daemonset_list =client_api.list_daemon_set_for_all_namespaces(watch=True)
            data=__format_data_for_daemonset(daemonset_list)
            #print("Daemonset under all namespaces: {}".format(data))
            return data
        else:
            daemonset_list = client_api.list_namespaced_daemon_set(namespace)
            data=__format_data_for_daemonset(daemonset_list)
            #print("Daemonset under default namespaces: {}".format(data))
            return data