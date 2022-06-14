from kubernetes import client
from kubernetes import client, config
from kubernetes.client import ApiClient
from os import path
import yaml
from kubernetes.client.rest import ApiException



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


def __format_data_for_statefulset(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for statefullset in json_data["items"]:
                temp_dict={
                    "statefullset": statefullset["metadata"]["name"],
                    "namespace": statefullset["metadata"]["namespace"],
                }
                temp_list.append(temp_dict)
        return temp_list

def get_statefulsets(cluster_details,namespace="default",all_namespaces=True):    
        client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            statefulset_list =client_api.list_stateful_set_for_all_namespaces(watch=False)
            data=__format_data_for_statefulset(statefulset_list)
            print("statefullset Set under all namespaces: {}".format(data))    
            return data
        else:
            statefulset_list = client_api.list_namespaced_stateful_set(namespace)
            data=__format_data_for_statefulset(statefulset_list)
            print("statefullset Set under namespaces {}: {}".format(namespace,data))            
            return data

def create_service(cluster_details):
    client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="redis-test-svc"
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "redis"},
            cluster_ip="None",
            type="ClusterIP",
            ports=[client.V1ServicePort(
                port=6379,
                target_port=6379
            )]
        )
    )
    # Create the service in specified namespace
    # (Can replace "default" with a namespace you may have created)
    client_api.create_namespaced_service(namespace="default", body=body)


def create_stateful_set_object(cluster_details):
    client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    container = client.V1Container(
        name="sts-redis",
        image="redis",
        image_pull_policy="IfNotPresent",
        ports=[client.V1ContainerPort(container_port=6379)],
    )
    # Template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "redis"}),
        spec=client.V1PodSpec(containers=[container]))
    # Spec
    spec = client.V1StatefulSetSpec(
        replicas=1,
        service_name="redis-test-svc",
        selector=client.V1LabelSelector(
            match_labels={"app": "redis"}
        ),
        template=template)
    statefulset = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name="statefulset-redis"),
        spec=spec)
    client_api.create_namespaced_stateful_set(
        namespace="default", body=statefulset
            )



#create, update, delete function for statefulsets yaml


def create_stateful_sets(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_appsv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )

    
        resp = client_api.create_namespaced_stateful_set(body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_statefulset(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN create_statefulsets:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))


def update_stateful_set(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_appsv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.patch_namespaced_stateful_set(
            body=yaml_body,
            namespace="{}".format(namespace))
        data=__format_data_for_statefulset(resp)
        print("DATA:{}".format(data))
        print("TYPE:{}".format(type(data)))
    except ApiException as e:
        print("ERROR IN update_statefulsets:\n{}".format(e.body))
        print("TYPE:{}".format(type(e)))



def delete_stateful_sets(cluster_details,sts_name,namespace="default"):
    try:
        client_api= __get_kubernetes_appsv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp=client_api.delete_namespaced_stateful_set(
            name=sts_name, namespace="{}".format(namespace))
        print("RESPONSE:{}".format(resp))
        print("TYPE:{}".format(type(resp)))
    except ApiException as e:
        print("ERROR IN delete_statefulsets:\n{}".format(e.body))
        print("TYPE:{}".format(e))
        

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlYxVWh2RUFSYnZPX1Nka0VTdExRVUNpYnhhdnR5WVNQVmtuYXdMMGFyekUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1jbHVzdGVyLXJvbGUtdG9rZW4tbXN3bngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWNsdXN0ZXItcm9sZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjJmZTVkNjg4LWM5NjAtNDE4Yy04MWEyLTcyNTJiZDIwNWRhNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRhc2hib2FyZC1jbHVzdGVyLXJvbGUifQ.t7gBKdpf6jZNXLswm3aHS_3Gu_PLzuLVBVLx_4gOcxHkyaIJ-vJFj8gSVzSBAmW56D3Rq_tpSVAWPauXv4Cca11PJ9O3ZI_6yuCDRXZre7EcmFDOPrlTjQwH-63mH4ItdWMwqLD2HXABOtnRUwrtSMwBIurZJ53_U_O--XUFo9kxTGqMAyeNY7kCACutHwZeCIXchYQ9WMku01vKLcSyV4p5SdK3Wk6ek-CbyN4fScSfQStgsFN37CV2ssNZTThbi3PXzXVMuKnUQXUzYLSwe46kvvLGnaCIYqRgxWpGMSnHlh--pws73-QKLRFmvO_HOLFDnBOe_06yEJ8i47YP9Q"
API = "https://34.123.166.9"
cluster = {
    "bearer_token" : TOKEN,
    "api_server_endpoint" : API
}
delete_stateful_sets(cluster , sts_name=cockpit-1)


