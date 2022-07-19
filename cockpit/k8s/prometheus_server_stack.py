from kubernetes import client
import yaml
from kubernetes.client import ApiClient
import os
import time

def deploy_prometheus_server_stack(cluster_details,manifest_path="{}/prometheus".format(os.getenv("MANIFEST_PATH","/manifest")),namespace="default"):
    try:
        PROMETHEUS_ENDPOINT = 'None'
        configuration = client.Configuration()
        configuration.host = cluster_details["api_server_endpoint"]
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + cluster_details["bearer_token"]}
        client.Configuration.set_default(configuration)

        #SERVICE_ACCOUNT
        service_account_api=client.CoreV1Api()
        service_account=(
            "alert-manager-serviceaccount.yaml",
            "kube-metrics-serviceaccount.yaml",
            "node-exporter-serviceaccount.yaml",
            "prometheus-server-serviceaccount.yaml",
            "pushgateway-serviceaccount.yaml"
            )
        for i in service_account:
            service_account_file_path="{}/{}".format(manifest_path,i)
            with open(service_account_file_path) as f:
                yaml_file = yaml.safe_load(f)
                service_account_api.create_namespaced_service_account(body=yaml_file,namespace=namespace)
        
        #CONFIGMAPS
        k8s_apps_v1  = client.CoreV1Api()
        configmap=(
            "alert-manager-cm.yaml",
            "prometheus-server-cm.yaml"
            )
        for i in configmap:
            configmap_file_path="{}/{}".format(manifest_path,i)
            with open(configmap_file_path) as f:
                yaml_body= yaml.safe_load(f)
                k8s_apps_v1.create_namespaced_config_map(body=yaml_body,namespace="default")
        #PVC        
        pvc = (
            "alert-manager-pvc.yaml",
            "prometheus-server-pvc.yaml"
            )
        for i in pvc:
            pvc_file_path="{}/{}".format(manifest_path,i)
            with open(pvc_file_path) as f:
                yaml_file = yaml.safe_load(f)
                k8s_apps_v1.create_namespaced_persistent_volume_claim(body=yaml_file,namespace=namespace)
                
        # CLUSTERROLE
        rbac_api = client.RbacAuthorizationV1Api()
        clusterrole=(
            "alert-manager-clusterrole.yaml",
            "kube-metrics-clusterrole.yaml",
            "prometheus-server-clusterrole.yaml",
            "pushgateway-clusterrole.yaml"
        )
        for i in clusterrole:
            clusterrole_file_path="{}/{}".format(manifest_path,i)
            with open(clusterrole_file_path) as f:
                yaml_file = yaml.safe_load(f)
                rbac_api.create_cluster_role(yaml_file)

        #CLUSTEROLE_BINDING
        clusterrole_binding=(
            "alert-manager-clusterrolebinding.yaml",
            "kube-metrics-clusterrolebinding.yaml",
            "prometheus-server-clusterrolebinding.yaml",
            "pushgateway-clusterrolebinding.yaml"
        )
        for i in clusterrole_binding:
            clusterrolebinding_file_path="{}/{}".format(manifest_path,i)
            with open(clusterrolebinding_file_path) as f:
                yaml_file = yaml.safe_load(f)
                rbac_api.create_cluster_role_binding(yaml_file)

        #SERVICE
        service_client_api = client.CoreV1Api()
        service=(
            "kube-metrics-service.yaml",
            "alert-manager-service.yaml",
            "node-exporter-service.yaml",
            "pushgateway-service.yaml",
            "prometheus-server-service.yaml"
        )
        for i in service:
            service_file_path="{}/{}".format(manifest_path,i)
            with open(service_file_path) as f:
                yaml_file = yaml.safe_load(f)
                service_client_api.create_namespaced_service(body=yaml_file,namespace=namespace)

        # #DAEMONSET
        k8s_apps_v1  = client.AppsV1Api()
        daemonset=("node-exporter-daemonset.yaml")
        daemonset_file_path="{}/{}".format(manifest_path,daemonset)
        with open(daemonset_file_path) as f:
            yaml_body= yaml.safe_load(f)
            k8s_apps_v1.create_namespaced_daemon_set(body=yaml_body,namespace="default")
        
        #DEPLOYMENT
        k8s_apps_v1  = client.AppsV1Api()
        deployment=(
            "kube-metrics-deployment.yaml",
            "alert-manager-deployment.yaml",
            "prometheus-server-deployment.yaml",
            "pushgateway-deployment.yaml"
            )
        for i in deployment:
            deployment_file_path="{}/{}".format(manifest_path,i)
            with open(deployment_file_path) as f:
                yaml_body= yaml.safe_load(f)
                k8s_apps_v1.create_namespaced_deployment(body=yaml_body,namespace="default")

        # #ingress
        ingress_client_api = client.NetworkingV1Api()

        ingress=("ingress.yaml")
        ingress_file_path="{}/{}".format(manifest_path,ingress)

        time.sleep(60)

        with open(ingress_file_path) as f:
            yaml_file = yaml.safe_load(f)
            ingress_client_api.create_namespaced_ingress(body=yaml_file,namespace="default")

        
        name='cockpit-prometheus'
        client_output=ingress_client_api.read_namespaced_ingress(name, namespace)
        json_data=ApiClient().sanitize_for_serialization(client_output)
        print("INGRESS RESPONE:{}".format(json_data['status']))
        PROMETHEUS_ENDPOINT= json_data['status']['loadBalancer']['ingress'][0]['ip']
        data={
            'message': 'Successfully',
            'code': 4005,
            'prometheus_server_endpoint':'http://{}'.format(PROMETHEUS_ENDPOINT)
        }
        return data
    except Exception as e:
        print("Error Deploying Prometheus Stack \n{}".format(e))
        data={
            'message': 'Failed',
            'code': 4006,
            'prometheus_server_endpoint':'None'
        }
        return data