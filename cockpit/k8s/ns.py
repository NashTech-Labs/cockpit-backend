from kubernetes import client
from kubernetes.client import ApiClient
import json
from kubernetes.client.rest import ApiException

def __get_kubernetes_batchv1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.BatchV1Api()
        return client_api
    except Exception as e:
        #print("Error getting kubernetes client \n{}".format(e))
        return None


def __format_data_for_create_cronjob(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list


def get_namespace(cluster_details,namespace="default",all_namespaces=False):

    try:
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        res=client_api.list_namespace()

        data=__format_data_for_create_cronjob(res)
        print(data) 
        # print("list of all namespaces :{}".format(res))
    except ApiException as e:
        print("ERROR IN getting_namespace:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))