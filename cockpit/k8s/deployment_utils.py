from kubernetes import client
from kubernetes.client import ApiClient
import yaml
from os import path

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

def __format_data_for_deployment(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for deploy in json_data["items"]:
                temp_dict={
                    "deployment": deploy["metadata"]["name"],
                    "namespace": deploy["metadata"]["namespace"],
                }
                temp_list.append(temp_dict)
        return temp_list

def get_deployments(cluster_details,namespace="default",all_namespaces=True):    
        client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            deploy_list =client_api.list_deployment_for_all_namespaces(watch=False)
            data=__format_data_for_deployment(deploy_list) 
            print("Deployment Set under all namespaces: {}".format(data))    
            return data
        else:
            deploy_list = client_api.list_namespaced_deployment(namespace)
            data=__format_data_for_deployment(deploy_list) 
            print("DeploySet under namespaces {}: {}".format(namespace,data))            
            return data

def create_deployment_object(DEPLOYMENT_NAME, image_name, port, resource, labels, container_name):
    # Configureate Pod template container
    container = client.V1Container(
        name=container_name,
        image=image_name,
        ports=[client.V1ContainerPort(container_port=port)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": resource['request']['cpu'], "memory": resource['request']['memory']},
            limits={"cpu": resource['limits']['cpu'], "memory": resource['limits']['memory']},
        ),
    )

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={labels['key']: labels['value']}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3, template=template, selector={
            "matchLabels":
            {labels['key']: labels['value']}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec,
    )

    return deployment


def create_deployment(cluster_details, deployment, ns):
    client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    resp = client_api.create_namespaced_deployment(
        body=deployment, namespace=ns
    )

    print("Deployment created. status='%s'" % resp.metadata.name)

    
    # update_deployment


def update_deployment(cluster_details, deployment, ns, DEPLOYMENT_NAME, replicas, image_name):
    client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    deployment.spec.template.spec.containers[0].image = image_name
    deployment.spec.replicas = replicas

    # patch the deployment
    resp = client_api.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME, namespace=ns, body=deployment
    )
    print("Deployment updated. status='%s'" % resp.metadata.name)

#    delete_deployment

def delete_deployment(cluster_details, ns, DEPLOYMENT_NAME):
    client_api= __get_kubernetes_appsv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
    resp = client_api.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace=ns,
        body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        ),
    )
    print("Deployment deleted")




#  by using yaml file

    # def create_deployment(cluster_details):
#     client_api= __get_kubernetes_appsv1client(
#             bearer_token=cluster_details["bearer_token"],
#             api_server_endpoint=cluster_details["api_server_endpoint"],
#         )
#     with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
#         dep = yaml.safe_load(f)
#         resp = client_api.create_namespaced_deployment(
#             body=dep, namespace="default")
#         print("Deployment created. status='%s'" % resp.metadata.name)

# create_deployment(cluster_details)