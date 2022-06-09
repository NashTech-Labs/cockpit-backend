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

def create_daemon_set_object():
    container = client.V1Container(
        name="ds-redis",
        image="redis",
        image_pull_policy="IfNotPresent",
        ports=[client.V1ContainerPort(container_port=6379)],
    )
    # Template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "redis"}),
        spec=client.V1PodSpec(containers=[container]))
    # Spec
    spec = client.V1DaemonSetSpec(
        selector=client.V1LabelSelector(
            match_labels={"app": "redis"}
        ),
        template=template)
    # DaemonSet
    daemonset = client.V1DaemonSet(
        api_version="apps/v1",
        kind="DaemonSet",
        metadata=client.V1ObjectMeta(name="daemonset-redis5"),
        spec=spec)

    return daemonset

def create_daemon_set(cluster_details,apps_v1_api, daemon_set_object):
    # Create the Daemonset in default namespace
    # You can replace the namespace with you have created
    client_api=__get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    api_response=client_api.create_namespaced_daemon_set(
        namespace="default", body=daemon_set_object
    )
    print("Daemonset created. status='%s'" % str(api_response.status))