from kubernetes import client, config
from kubernetes.client import ApiClient


JOB_NAME = "pi"

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
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_job(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for job in json_data["items"]:
                temp_dict={
                    "job": job["metadata"]["name"],
                    "namespace": job["metadata"]["namespace"],
                    "status": job["status"]["phase"]
                }
                temp_list.append(temp_dict)
        return temp_list

def get_jobs(cluster_details,namespace="default",all_namespaces=True):
        client_api= __get_kubernetes_batchv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            job_list =client_api.list_job_for_all_namespaces(watch=False)
            data=__format_data_for_job(job_list)
            print("Jobs under all namespaces: {}".format(data))
            return data
        else:
            job_list = client_api.list_namespaced_job(namespace)
            data=__format_data_for_job(job_list)
            print("jobs under namespaces {}: {}".format(namespace,data))
            return data



def create_job_object(cluster_details):
    client_api= __get_kubernetes_batchv1client(
        bearer_token=cluster_details["bearer_token"],
        api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    container = client.V1Container(
        name="pi",
        image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)
    api_response = client_api.create_namespaced_job(
        body=job,
        namespace="default")

    return api_response



