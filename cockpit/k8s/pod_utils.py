from kubernetes import client
from kubernetes.client import ApiClient
import json
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

def __format_data_for_create_pod(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
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

def create_pod(cluster_details,yaml_body=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.create_namespaced_pod(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_pod(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_pod(e.body)

def update_pod(cluster_details,k8s_object_name=None,yaml_body=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.patch_namespaced_pod(
            name=k8s_object_name,
            body=yaml_body, 
            namespace="{}".format(namespace))

        data=__format_data_for_create_pod(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_pod(e.body)

def delete_pod(cluster_details,k8s_object_name=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.delete_namespaced_pod(
                name=k8s_object_name,
                namespace="{}".format(namespace),
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5)
            )

        data=__format_data_for_create_pod(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_pod(e.body)


def _get_pod_logs(pod_name=None, namespace=None,client_api=None,container=None):
    try:
        api_response = client_api.read_namespaced_pod_log(name=pod_name, namespace=namespace,container=container)
        # print('#############################')
        # print(api_response)
        # print('#############################')
        # print("Data type:{}".format(type(api_response)))
        data={container:api_response}

        return data
    except ApiException as e:
        print('Found exception in reading the logs {}'.format(e.body))
        return {container:""}
    

def _get_pod_events(pod_name=None, namespace=None,client_api=None):
    pass

def get_specific_pod_details(cluster_details,namespace="default",k8_object_name=None):

    """
    {
    "resource_name":"some-pod",
    "namespace": "default",
    "resource_kind": "Pod",
    "events": " Some Events",
    "live_manifest": {},
    "logs": [{'container:'logs''}]
    }
    """

    try:
        response_data={
            'resource_name': '{}'.format(k8_object_name),
            'namespace': '{}'.format(namespace),
            "resource_kind": "Pod",
            'events':[],
            'live_manifest': {}
        }

        logs=[]
        events=[]
        client_api= __get_kubernetes_corev1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        pod_list = client_api.list_namespaced_pod(namespace)
        pod_data={}
        data=__format_data_for_pod(pod_list)
        for pod in data:
            if pod['pod'] == k8_object_name:
                pod_data=pod
                break
        print("POD DATA:{}".format(pod_data))
        for container in pod_data['containers']:
            container_name=container['name']
            log = _get_pod_logs(pod_name=k8_object_name,namespace=namespace,client_api=client_api,container=container_name)
            logs.append(log)
        response_data.update({'logs':logs})

        # events=_get_pod_events(pod_name=pod_name,namespace=namespace,client_api=client_api)
        
        #print("Pods under namespaces {}: {}".format(namespace,data))
        return response_data
    except ApiException as e:
        print("ERROR IN getting pod specific details:\n{}".format(e.body))
        response_data={
            'resource_name': '{}'.format(k8_object_name),
            'namespace': '{}'.format(namespace),
            "resource_kind": "Pod",
            'events':[],
            'logs':[],
            'live_manifest': {}
        }
        return response_data  