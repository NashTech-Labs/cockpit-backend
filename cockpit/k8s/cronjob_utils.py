from kubernetes import client
from kubernetes.client import ApiClient

from time import sleep

import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config


JOB_NAME = "pi"

#get kuberenetes client for listing cronjobs
def __get_kubernetes_batchv1client(bearer_token,api_server_endpoint):
    try:
        #corev1api=("pod","node","config_map","secret","service","namespace","resource")
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

def __format_data_for_cronjob(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for cronjob in json_data["items"]:
                temp_dict={
                    "cronjob": cronjob["metadata"]["name"],
                    "namespace": cronjob["metadata"]["namespace"],
                    "status": cronjob["status"]["phase"]
                }
                temp_list.append(temp_dict)
        return temp_list

def get_cronjobs(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_batchv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            cronjob_list =client_api.list_cron_job_for_all_namespaces(watch=False)
            data=__format_data_for_cronjob(cronjob_list)
            #print("cronjob under all namespaces: {}".format(data))
            return data
        else:
            cronjob_list = client_api.list_namespaced_cron_job("{}".format(namespace))
            data=__format_data_for_cronjob(cronjob_list)
            #print("cronjob under namespaces {}:{}".format(namespace,data))
            return data


#get kuberenetes client for creating cronjobs
def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.BatchV1beta1Api(api_client)
        return api_instance1
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def create_cron_job(api_instance,cluster_details,namespace):
    container = client.V1Container(
    name="pi",
    image="perl",
    command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)  #specify the number of retries before considering a Job as failed
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)


    client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )

    api_response = client_api.create_namespaced_cron_job(
        body=client.V1beta1CronJob(
            api_version='batch/v1beta1',
            kind='CronJob',
            metadata=client.V1ObjectMeta(name='cronjob9'),
            spec = client.V1CronJobSpec(

                schedule="25 17 8 6 2", #     25(minute)   5(pm)   8(date)   june(month) tuesday(day of the week)
                job_template=job
            )
            
        ),
        namespace=namespace)
    print("cronJob created. status='%s'" % str(api_response.status))