from kubernetes import client
import yaml
import os

def deploy_ingress_controller_stack(cluster_details,manifest_path="{}/ingress-controller".format(os.getenv("MANIFEST_PATH","/manifest")),namespace="default"):

    try:
    
        configuration = client.Configuration()
        configuration.host = cluster_details["api_server_endpoint"]
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + cluster_details["bearer_token"]}
        client.Configuration.set_default(configuration)

        #service account
        service_account_api = client.CoreV1Api()
        serviceaccount=(
            "controller-serviceaccount.yaml"
            ,"serviceaccount.yaml"
        )
        for i in serviceaccount:
            serviceaccount_file_path="{}/{}".format(manifest_path,i)
            with open(serviceaccount_file_path) as f:
                yaml_file = yaml.safe_load(f)
                service_account_api.create_namespaced_service_account(body=yaml_file,namespace="default")

        #cluster role
        cluster_role_api = client.RbacAuthorizationV1Api()
        cluster_role=(
            "clusterrole.yaml",
            "controller-clusterrole.yaml"
            )
        for i in cluster_role:
            cluster_role_file_path="{}/{}".format(manifest_path,i)
            with open(cluster_role_file_path) as f:
                yaml_file = yaml.safe_load(f)
                cluster_role_api.create_cluster_role(yaml_file)
        
        #cluster role binding
        cluster_role_binding_api = client.RbacAuthorizationV1Api()
        cluster_role_binding=(
            "clusterrolebinding.yaml",
            "controller-clusterrolebinding.yaml"
            )
        for i in cluster_role_binding:
            cluster_role_binding_file_path="{}/{}".format(manifest_path,i)
            with open(cluster_role_binding_file_path) as f:
                yaml_file = yaml.safe_load(f)
                cluster_role_binding_api.create_cluster_role_binding(yaml_file)
        #role
        role_client_api = client.RbacAuthorizationV1Api()
        role=(
            "controller-role.yaml",
            "role.yaml"
            )
        for i in role:
            role_file_path="{}/{}".format(manifest_path,i)
            with open(role_file_path) as f:
                yaml_file = yaml.safe_load(f)
                role_client_api.create_namespaced_role(body=yaml_file,namespace="default")
        
        #rolebinding
        rolebinding_api = client.RbacAuthorizationV1Api()
        rolebinding=(
            "controller-rolebinding.yaml",
            "rolebinding.yaml"
            )
        for i in rolebinding:
            role_file_path="{}/{}".format(manifest_path,i)
            with open(role_file_path) as f:
                yaml_file = yaml.safe_load(f)
                rolebinding_api.create_namespaced_role_binding(body=yaml_file,namespace="default")

        job_api = client.BatchV1Api()
        job=(
            "job-createSecret.yaml",
            "job-patchWebhook.yaml"
        )
        for i in job:
            job_file_path="{}/{}".format(manifest_path,i)
            with open(job_file_path) as f:
                yaml_body= yaml.safe_load(f)
                job_api.create_namespaced_job(body=yaml_body,namespace="default")

        config_map_api = client.CoreV1Api()
        config_map=["controller-configmap.yaml"]
        for i in config_map:
            config_map_file_path="{}/{}".format(manifest_path,i)
            with open(config_map_file_path) as f:
                yaml_file = yaml.safe_load(f)
                config_map_api.create_namespaced_config_map(body=yaml_file,namespace="default")

        service_api = client.CoreV1Api()
        service=(
            "controller-service.yaml",
            "controller-service-webhook.yaml"
            )
        for i in service:
            service_file_path="{}/{}".format(manifest_path,i)
            with open(service_file_path) as f:
                yaml_file = yaml.safe_load(f)
                service_api.create_namespaced_service(body=yaml_file,namespace="default")

        deployment_api = client.AppsV1Api()
        deployment=["controller-deployment.yaml"]
        for i in deployment:
            deployment_file_path="{}/{}".format(manifest_path,i)
            with open(deployment_file_path) as f:
                yaml_file = yaml.safe_load(f)
                deployment_api.create_namespaced_deployment(body=yaml_file,namespace="default")

        ingressclass_api = client.NetworkingV1Api()
        ingress_class=["controller-ingressclass.yaml"]
        for i in ingress_class:
            ingress_class_file_path="{}/{}".format(manifest_path,i)
            with open(ingress_class_file_path) as f:
                yaml_file = yaml.safe_load(f)
                ingressclass_api.create_ingress_class(body=yaml_file)

        webhook_api = client.AdmissionregistrationV1Api()
        webhook=["validating-webhook.yaml"]
        for i in webhook:
            webhook_file_path="{}/{}".format(manifest_path,i)
            with open(webhook_file_path) as f:
                yaml_body= yaml.safe_load(f)
                webhook_api.create_validating_webhook_configuration(body=yaml_body)

        data={
            'message': 'Successfully',
            'code': 4002,
            'ingress_controller_endpoint':'{}'.format("127.0.0.1")
        }
        return data
    except Exception as e:
        print("Error creating webhook configuration \n{}".format(e))
        data={
            'message': 'Failed',
            'code': 4003,
            'ingress_controller_endpoint':'{}'.format("127.0.0.1")
        }
        return data
if __name__ == '__main__':
    cluster_details={
        "bearer_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6ImZNQlJPMk9EeUY4M0d4UmRnUWZqMnJDcTRZcDVzOHdqXzFmd2pRanBacDQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImNoYXJ0MS10b2tlbi1jNmRrYiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJjaGFydDEiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJiM2IwYTJjYi1hNjQxLTRlOTgtODVkZS1mM2Q1ZjE1OWJmMzciLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpjaGFydDEifQ.RlXtKslsCchcS3s60AsG3xtlXpUc1Z4gvfQFGqU4Q7WFUYpWmBRqqtEyQULEXY6JLRgXXkHY2WmgIPeppeKPlyC9pDvg9RjLY-9D6Zh64Nhu2EQy4KSu0Kgrs9oT8cg5EP37Cr2xX91zTc81cyx0el4kxPoPDVZuTrlTj1rmqzU1q_O6-WT4-QTpj87KY9jZs2aIuyCdPVBoifinSLI_m4gkFuTeptNOcZApPgjT0oYngoT0xBgC-x_RZTFHADkA_bpcgJn2wFyetNNLcECGGpuRnJrXfJ0cVxOfW0CHZSyeaBRL_06o49mnbVZ8oNTdACe91wAQqV5KdYUCXASGug",
        "api_server_endpoint":"https://192.168.49.2:8443"
    }
