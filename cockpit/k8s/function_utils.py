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
            )

GET_ACTIONS_JSON= {
            "get-pod":get_pods,
            "get-deployment":get_deployments,
            "get-daemonset":get_daemonsets,
            "get-cronjob":get_cronjobs,
            "get-job":get_jobs,
            "get-statefullset":get_statefulsets,
            "get-replicaset":get_replicasets,
            # "get-configmap",
            # "get-secret",
            # "get-namespace:",
        }
