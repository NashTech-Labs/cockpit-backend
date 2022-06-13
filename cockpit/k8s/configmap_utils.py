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




#create function for Config Map

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


# data={
#     "app": "cockpit"
# }
#create_config_map(cluster_details,data)



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

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlpQYVBWbm5Kb1FMN0NFMzR3MnlSbXE1R3hlQ3RfTDVQZWNBQmVmSUpNMFEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1jbHVzdGVyLXJvbGUtdG9rZW4tdnJtamsiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWNsdXN0ZXItcm9sZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjcwZGVlYjU1LWVmNDItNGQxNC05NjM3LThkYWFlZGU4NzYwNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRhc2hib2FyZC1jbHVzdGVyLXJvbGUifQ.kilBAHfo2iRdlILhZPFn0XDfSwz3rHSM15h46B9g4wgzt7EJWkvc1GwVhpmcPNmd4Kj_ePcWILJKtjZTQDknkjyNFzD2NeX3v92-LfEA1C5svljwBXFY3S4AUZCfWFhpYEV-qYGsTKqVgeWqGFpy9r8Sd4qkR_zecvAUdF_bRkDJZ7_JDp6BCqvoi_KDmyWxpeDEe6ueYa0KLAHdJMKcH3fmN4h9WnBuuEBg2Q0gEetxdui0cWbRWQQplhR7lP_-V364NmgJByesuT69VSL2CY_DGxb8XU4oFnChlNsHd_Qt3GMRUGrW3DxtHZrdtv34REBV_tR5UqtnVLQCAQpQJA"
API = "https://34.69.172.158"
cluster = {
    "bearer_token" : TOKEN,
    "api_server_endpoint" : API
}
cm={
    "name": "abcd"
}
delete_config_map(cluster , "deekasha-01")

