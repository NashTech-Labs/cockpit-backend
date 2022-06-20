
import json
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from kubernetes.client import ApiClient

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.CoreV1Api(api_client)
        return api_instance1

    except ApiException as e:
        print("Error getting kubernetes client:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return None


def __format_data_for_pod(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for ns in json_data["items"]:
                temp_dict={
                    "namespace": ns["metadata"]["name"]
                    
                }
                temp_list.append(temp_dict)
        return temp_list



def get_namespaces(cluster_details,namespace="default",all_namespaces=True):

    try:
        if all_namespaces is True:

            client_api= __get_kubernetes_client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
                )
            res=client_api.list_namespace()

            data=__format_data_for_pod(res)
            return data
        else:
            return []
    except Exception as e:
        return []