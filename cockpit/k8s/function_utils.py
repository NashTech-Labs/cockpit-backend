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
from .svc_utils import *

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

GET_ACTIONS=(   
            "get-pod",
            "get-namespace",
            "get-deployment",
            "get-daemonset",
            "get-cronjob",
            "get-job",
            "get-statefullset",
            "get-configmap",
            "get-secret",
            "get-replicaset"
            "get-service"
            )

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
            "get-service": get_service,
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
            "create-service":create_service,
            # "get-namespace:",
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
            "delete-service":delete_service,
            #"get-namespace:",
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
            "update-service":update_service,
            # # "get-namespace:",
        }