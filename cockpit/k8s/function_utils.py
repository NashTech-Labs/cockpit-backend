from .serializers import *
import json
from platforms.platform_state import *
from .pod_utils import *
from .cronjob_utils import *
from .daemonset_utils import *
from .statefullset_utils import *
from .job_utils import *
from .deployment_utils import *
from .replicaset_utils import *
from .configmap_utils import *
from .secret_utils import *
from .namespace_utils import *
from .service_uitls import *
from .ingress_utils import *
from .ingress_controller_stack import *
from .prometheus_server_stack import *
from cockpit.celery import app 

def check_cluster_existence(cluster_name):
    cluster_data= get_cluster_details(cluster_name=cluster_name)
    if len(cluster_data) == 0 :
        print("Cluster Does not Exists")
        data={
            "message": "{}".format(PLATFORM_STATE[3001]),
            "status_code":3001,
            "cluster_name":"{}".format(cluster_name)
        }
        return data
    else:
        print("Cluster Already Exists")
        data={
            "message": "{}".format(PLATFORM_STATE[3000]),
            "status_code":3000,
            "cluster_name":"{}".format(cluster_name),
            "version":"{}".format(cluster_data["version"])
        }
        return data

def check_for_monitoring_status(cluster_name):
    monitoring_data=get_monitoring_details(cluster_name=cluster_name)
    if len(monitoring_data) == 0 :
        print("Monitoring Request Does not Exists")
        data={
            "message": "{}".format(PLATFORM_STATE[4000]),
            "monitoring_state":4000,
            "cluster_name":"{}".format(cluster_name),
            "prometheus_server_url":'None',
            "grafana_dashboard_url":"None"
        }
        return data
    else:
        monitoring_state=monitoring_data["monitoring_state"]
        print("Monitoring Request Exists, State: {}".format(PLATFORM_STATE[monitoring_state]))
        data={
            'message':'{}'.format(PLATFORM_STATE[monitoring_state]),
            'monitoring_state':'{}'.format(monitoring_state),
            'cluster_name': '{}'.format(cluster_name),
            'grafana_dashboard_url':'{}'.format(monitoring_data["grafana_dashboard_url"])            
        }
        return data


@app.task(time_limit=600,queue='default')
def enable_monitoring(cluster_details):
    try:
        cluster_name=cluster_details["cluster_name"]

        monitoring_details={
            'cluster_name': cluster_name,
            'prometheus_server_url': 'None',
            'grafana_dashboard_url' : 'None',
            'monitoring_state': 4001,
            'message': 'None'
        }
        ingress_controller_data=deploy_ingress_controller_stack(cluster_details)

        if ingress_controller_data["code"] == 4002:

            monitoring_details.update(
                monitoring_state=4002,
                message=PLATFORM_STATE[4002]
                )
            update_monitoring_details(monitoring_details)
            prometheus_server_data=deploy_prometheus_server_stack(cluster_details)

            if prometheus_server_data["code"] == 4006:
                monitoring_details.update(
                    monitoring_state=4006,
                    message=PLATFORM_STATE[4006]
                    )
                update_monitoring_details(monitoring_details)
            else:
                monitoring_details.update(
                    monitoring_state=4006,
                    message=PLATFORM_STATE[4006],
                    prometheus_server_url=prometheus_server_data['prometheus_server_endpoint']
                )
                update_monitoring_details(monitoring_details)

        else:
            monitoring_details.update(
                monitoring_state=4007,
                message=PLATFORM_STATE[4003],
                prometheus_server_url='None'
            )
            update_monitoring_details(monitoring_details)

        
    except Exception as e:
        print("Error in Enable Monitoring \n {}".format(e))


# GET_ACTIONS=(   
#             "get-pod",
#             "get-namespace",
#             "get-deployment",
#             "get-daemonset",
#             "get-cronjob",
#             "get-job",
#             "get-statefullset",
#             "get-configmap",
#             "get-secret",
#             "get-replicaset"
#             )

GET_ACTIONS_JSON= {
            "get-pod":get_pods,
            "get-deployment":get_deployments,
            "get-daemonset":get_daemonsets,
            "get-cronjob":get_cronjobs,
            "get-job":get_jobs,
            "get-statefulset":get_statefulsets,
            "get-replicaset":get_replicasets,
            "get-configmap":get_configmaps,
            "get-secret":get_secrets,
            "get-namespace": get_namespaces,
            "get-service":get_services,
            "get-ingress": get_ingress,
        }

CREATE_ACTIONS_JSON= {
            "create-pod":create_pod,
            "create-deployment":create_deployment,
            "create-daemonset":create_daemonset,
            "create-cronjob":create_cronjob,
            "create-job":create_job,
            #"create-statefulset":create_statefulset,
            "create-replicaset":create_replicaset,
            "create-configmap":create_configmap,
            "create-secret":create_secret,
            "create-service": create_service,
            "create-ingress": create_ingress,
            # "create-namespace:",
        }

DELETE_ACTIONS_JSON= {
            "delete-pod":delete_pod,
            "delete-deployment":delete_deployment,
            "delete-daemonset":delete_daemonset,
            "delete-cronjob":delete_cronjob,
            "delete-job":delete_job,
            # #"delete-statefulset":delete_statefulset,
            "delete-replicaset":delete_replicaset,
            "delete-configmap":delete_configmap,
            "delete-secret":delete_secret,
            "delete-service": delete_service,
            "delete-ingress": delete_ingress,
            #"delete-namespace:",
        }

UPDATE_ACTIONS_JSON= {
            "update-pod":update_pod,
            "update-deployment":update_deployment,
            "update-daemonset":update_daemonset,
            "update-cronjob":update_cronjob,
            "update-job":update_job,
            # #"update-statefulset":update_statefulset,
            "update-replicaset":update_replicaset,
            "update-configmap":update_configmap,
            "update-secret":update_secret,
            "update-service": update_service,
            "update-ingress": update_ingress,
            #"update-namespace:",
        }