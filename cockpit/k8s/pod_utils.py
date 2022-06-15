from os import path
from kubernetes import client
from kubernetes.client import ApiClient
from sympy import re
import yaml
from kubernetes.client.rest import ApiException 

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

# pod creation with yaml 


def create_pod(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )

    
        resp = client_api.create_namespaced_pod(body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_pod(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN create_pod:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))


def delete_pod(cluster_details,pod_name,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp=client_api.delete_namespaced_pod(
            name=pod_name, namespace="{}".format(namespace))
        print("RESPONSE:{}".format(resp))
        print("TYPE:{}".format(type(resp)))
    except ApiException as e:
        print("ERROR IN delete_pod:\n{}".format(e.body))
        print("TYPE:{}".format(e))

def update_pod(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.patch_namespaced_pod(
            body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_pod(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN update_pod:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))





# pod creation with generated manifest using k8s client


#user input must be like this
# pod_details={
#        "pod_name":"demo",
#        "image":"nginx",
#        "namespace":"default"
 
#     }

# def create_pod(cluster_details,pod_details):
#         client_api= __get_kubernetes_corev1client(
#              bearer_token=cluster_details["bearer_token"],
#              api_server_endpoint=cluster_details["api_server_endpoint"],
#          )
#         container = client.V1Container(
#             name=pod_details["pod_name"],
#             image=pod_details["image"],
#             # command=['bash', '-c'],
#             # args=[client_api.test_command],
#             image_pull_policy='Always',
#             # working_dir=client_api.working_dir,
#             stdin=True,
#             tty=True
#         )
#         pod_spec = client.V1PodSpec(
#             containers=[container],
#             restart_policy='Never'
#         )
#         pod = client.V1Pod(
#             api_version="v1",
#             kind="Pod",
#             metadata=client.V1ObjectMeta(name=pod_details["pod_name"]),
#             spec=pod_spec
#         )

#         try:
#             resp=client_api.create_namespaced_pod(pod_details["namespace"], pod)
#             print("pod created. status='%s'" % resp.metadata.name)
#         except client.rest.ApiException as e:
#             print("Got exception: {} while creating a pod".format(e))
#             return 1

#         return 0 


