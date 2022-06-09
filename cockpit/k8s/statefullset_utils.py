from kubernetes import client
from kubernetes import client, config
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
