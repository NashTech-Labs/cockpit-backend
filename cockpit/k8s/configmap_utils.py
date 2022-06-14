from sys import path_hooks
from kubernetes import client
from kubernetes.client import ApiClient
import yaml
from os import path
from kubernetes.client.rest import ApiException


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
    

# Get Function for Config Map

def get_configmaps(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            configmap_list =client_api.list_config_map_for_all_namespaces(watch=False)
            data=__format_data_for_configmap(configmap_list)
            return data
        else:
            configmap_list = client_api.list_namespaced_config_map(namespace)
            data=__format_data_for_configmap(configmap_list)
            return data


# Create function for Config Map

def create_config_map(cluster_details, cm_data):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(name="deekasha-01"),
        data=cm_data
    )

    api = client_api.create_namespaced_config_map(namespace="default", body=configmap)
    return api


# Create Function For Config Map using Yaml File

def create_config_map_yaml(cluster_details, path_configmap):

    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )

    with open(path.join(path.dirname(__file__), path_configmap)) as f:
        dep = yaml.safe_load(f)
        # k8s_apps_v1 = client.CoreV1Api(client_api)
        resp = client_api.create_namespaced_config_map(
            body=dep, namespace="default")


# Update Function for Config Map

def update_config_map(cluster_details, cm_data , name):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(name="deekasha-01"),
        data=cm_data
    )
    #api1 = client_api.patch_namespaced_config_map(name=name , namespace="default", body={})
    api = client_api.patch_namespaced_config_map(name=name , namespace="default", body=configmap)
    return api


# Update Function for Config Map Using Yaml

def update_config_map_yaml(cluster_details, path_configmap):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    with open(path.join(path.dirname(__file__), path_configmap)) as f:
        dep = yaml.safe_load(f)
        # k8s_apps_v1 = client.CoreV1Api(client_api)
        resp = client_api.create_namespaced_config_map(
            body=dep, namespace="default")


# Delete Function for Config Map

def delete_config_map(cluster_details , name):
    client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    #api1 = client_api.patch_namespaced_config_map(name=name , namespace="default", body={})
    api = client_api.delete_namespaced_config_map(name=name , namespace="default", body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5))
    return api



# CREATE, UPDATE, DELETE FUNCTION FOR CONFIG MAP YAML


def create_configmaps(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )

    
        resp = client_api.create_namespaced_config_map(body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_configmap(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN create_config_map:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))


def update_configmaps(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.patch_namespaced_config_map(
            body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_configmap(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN update_config_map:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))


def delete_configmaps(cluster_details,configmap_name,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp=client_api.delete_namespaced_config_map(
            name=configmap_name, namespace="{}".format(namespace))
        print("RESPONSE:{}".format(resp))
        print("TYPE:{}".format(type(resp)))
    except ApiException as e:
        print("ERROR IN delete_config_map:\n{}".format(e.body))
        print("TYPE:{}".format(e))


TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlYxVWh2RUFSYnZPX1Nka0VTdExRVUNpYnhhdnR5WVNQVmtuYXdMMGFyekUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1jbHVzdGVyLXJvbGUtdG9rZW4tbXN3bngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWNsdXN0ZXItcm9sZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjJmZTVkNjg4LWM5NjAtNDE4Yy04MWEyLTcyNTJiZDIwNWRhNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRhc2hib2FyZC1jbHVzdGVyLXJvbGUifQ.t7gBKdpf6jZNXLswm3aHS_3Gu_PLzuLVBVLx_4gOcxHkyaIJ-vJFj8gSVzSBAmW56D3Rq_tpSVAWPauXv4Cca11PJ9O3ZI_6yuCDRXZre7EcmFDOPrlTjQwH-63mH4ItdWMwqLD2HXABOtnRUwrtSMwBIurZJ53_U_O--XUFo9kxTGqMAyeNY7kCACutHwZeCIXchYQ9WMku01vKLcSyV4p5SdK3Wk6ek-CbyN4fScSfQStgsFN37CV2ssNZTThbi3PXzXVMuKnUQXUzYLSwe46kvvLGnaCIYqRgxWpGMSnHlh--pws73-QKLRFmvO_HOLFDnBOe_06yEJ8i47YP9Q"
API = "https://34.123.166.9"
cluster = {
    "bearer_token" : TOKEN,
    "api_server_endpoint" : API
}
cm={
    "name": "abcd"
}
delete_configmaps(cluster , configmap_name="deekashaaaa-03")

