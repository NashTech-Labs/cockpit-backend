from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponse, JsonResponse
from .function_utils import *
import json,base64,yaml
from platforms.platform_state import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import list_imported_cluster

import logging

#Get an instance of a specific named logger
logger = logging.getLogger('k8s-view')

@csrf_exempt
def get_cluster_imported_list(request):
    try:
        if request.method == 'GET':
            data=list_imported_cluster()
            return JsonResponse(data)
        else:
            return JsonResponse({"clusters":[],"message":"INVALID REQUEST METHOD"})
    except Exception as e:
        logger.exception("ERROR IN GET CLUSTER LIST:\n{}".format(e))
        return JsonResponse({"clusters":[],"message":"EXCEPTION IN LIST CLUSTERS"})

@csrf_exempt
def import_cluster(request):
    """
    {
        "cluster_name":"one_piece",
        "version":"1.22.8",
        "api_server_endpoint":"http://localhost",
        "bearer_token":"",
        "kubeconfig":"None",
        "cloud":"gke"
    }
    """
    try:
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))
            _temp_request_obj ={}
            _temp_request_obj.update(data)
            cluster_name=data["cluster_name"]
            check_data=check_cluster_existence(cluster_name=cluster_name)
            if check_data["status_code"] == 3000:
                #condition for cluster already exists
                return JsonResponse(check_data)
            else:
                create_kubernetes_config_entry_in_db(data)

                temp_data={
                        "message": "{}".format(PLATFORM_STATE[3001]),
                        "status_code":3001,
                        "cluster_name":"{}".format(cluster_name),
                        "version":"{}".format(data["version"]),
                    }
                return JsonResponse(temp_data)
        else:
            return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.error("Error in importing Cluster \n{}".format(e))
        return JsonResponse({"message":"Exception in import-cluster"})

@csrf_exempt
def get_cluster_api(request):
    """
    request_obj
    {
        "cluster_name":"one_piece",
        "action":"get_pod",
        "user_name": "monkey_d_luffy"
        "metadata":{
            "namespace":"default",
            "all_namespaces": "False",
        }
    }
    response_obj
    {
        "cluster_name":"one_piece",
        "action":"get-pod",
        "data":[{"pod":"1000-sunny","namespace":"default","status":"running"},{...}],
        "message":"list of pods under default",
        "status_code":0
    }
    """
    try:
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))
            _temp_request_obj ={}
            _temp_request_obj.update(data)
            cluster_name=data["cluster_name"]        
            api_function=GET_ACTIONS_JSON[data["action"]]
            cluster_details=get_cluster_details(cluster_name=cluster_name)
            response_data={
                "cluster_name":"{}".format(cluster_name),
                "action":"{}".format(data["action"])  
            }
            if len(cluster_details) == 0:
                response_data.update(
                    {
                        "message":"{}".format(PLATFORM_STATE[3404]),
                        "status_code":3404,
                        "data":[]
                    }
                )
                return JsonResponse(response_data)
            else:
                all_namespaces=data["metadata"]["all_namespaces"]
                namespace=data["metadata"]["namespace"]
                if all_namespaces == "False":
                    k8s_objects=api_function(cluster_details,namespace=namespace,all_namespaces=False)
                    response_data.update(
                        {
                            "message":"LIST KUBERNETES CLUSTER OBJECT",
                            "status_code":0,
                            "data":k8s_objects
                        }
                    )
                    return JsonResponse(response_data)
                else:
                    k8s_objects=api_function(cluster_details,all_namespaces=True)
                    response_data.update(
                        {
                            "message":"LIST ALL KUBERNETES CLUSTER OBJECTS",
                            "status_code":0,
                            "data":k8s_objects
                        }
                    )
                    return JsonResponse(response_data)
        else:
            return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.exception("Error in get cluster_api \n{}".format(e))
        data =json.loads(request.body.decode("utf-8"))
        response_data={
                            "message":"EXCEPTION IN GET KUBERNETES CLUSTER OBJECTS",
                            "status_code":1,
                            "data":[],
                            "cluster_name":"{}".format(data["cluster_name"]),
                            "action":"{}".format(data["action"])
                        }
                    
        return JsonResponse(response_data)


@csrf_exempt
def create_cluster_api(request):
    try:
        """
        Request_obj
        create-deployment

            {
                "cluster_name":"demo",
                "action":"create-deployment",
                "user_name": "monkey_d_luffy",
                "metadata":{
                    "namespace":"default",
                    "manifest" : "gtdZWxzOgogICAgICAgIGFwcDogbmdpbngtdGVzdHR0",
                    "k8s_object_name":""
                }
            }
            
        Response_obj

        {
            "cluster_name": "demo",
            "action": "create-deployment",
            "message": "CREATE KUBERNETES CLUSTER OBJECT",
            "status_code": 0,
            "data": []
        }
        """
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))

            _temp_request_obj ={}
            _temp_request_obj.update(data)

            cluster_name=data["cluster_name"]
            manifest=data["metadata"]["manifest"]
            yaml_data=base64.b64decode(manifest).decode('utf-8')
            yaml_body=yaml.safe_load(yaml_data)

            api_function=CREATE_ACTIONS_JSON[data["action"]]
            cluster_details=get_cluster_details(cluster_name=cluster_name)
            k8s_object_name=data["metadata"]["k8s_object_name"]

            response_data={
                "cluster_name":"{}".format(cluster_name),
                "action":"{}".format(data["action"])  
            }
            if len(cluster_details) == 0:
                response_data.update(
                    {
                        "message":"{}".format(PLATFORM_STATE[3404]),
                        "status_code":3404,
                        "data":[]
                    }
                )
                return JsonResponse(response_data)
            else:
                namespace=data["metadata"]["namespace"]
                k8s_objects=api_function(cluster_details,yaml_body=yaml_body,namespace=namespace)
                response_data.update(
                        {
                            "message":"CREATE KUBERNETES CLUSTER OBJECTS {}".format(k8s_object_name),
                            "status_code":0,
                            "data":k8s_objects
                        }
                    )
                return JsonResponse(response_data)
        else:
            return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.exception("Error in Create_cluster_api \n{}".format(e))
        data =json.loads(request.body.decode("utf-8"))
        response_data={
                            "message":"EXCEPTION IN CREATE KUBERNETES CLUSTER OBJECTS",
                            "status_code":1,
                            "data":[],
                            "cluster_name":"{}".format(data["cluster_name"]),
                            "action":"{}".format(data["action"])
                        }
                    
        return JsonResponse(response_data)

@csrf_exempt
def delete_cluster_api(request):
    """
    Request_obj
            {
                "cluster_name":"demo",
                "action":"delete-deployment",
                "user_name": "monkey_d_luffy",
                "metadata":{
                    "namespace":"default",
                    "k8s_object_name":""
                }
            }       
    Response_obj
        {
            "cluster_name": "demo",
            "action": "create-deployment",
            "message": "DELETE KUBERNETES CLUSTER OBJECT",
            "status_code": 0,
            "data": []
        }
    """

    try:
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))

            _temp_request_obj ={}
            _temp_request_obj.update(data)

            cluster_name=data["cluster_name"]

            api_function=DELETE_ACTIONS_JSON[data["action"]]
            cluster_details=get_cluster_details(cluster_name=cluster_name)

            k8s_object_name=data["metadata"]["k8s_object_name"]
            namespace=data["metadata"]["namespace"]

            response_data={
                "cluster_name":"{}".format(cluster_name),
                "action":"{}".format(data["action"])  
            }
            if len(cluster_details) == 0:
                response_data.update(
                    {
                        "message":"{}".format(PLATFORM_STATE[3404]),
                        "status_code":3404,
                        "data":[]
                    }
                )
                return JsonResponse(response_data)
            else:    
                k8s_objects=api_function(   cluster_details,
                                            k8s_object_name=k8s_object_name,
                                            namespace=namespace
                                        )
                response_data.update(
                        {
                            "message":"DELETE KUBERNETES CLUSTER OBJECTS {0}".format(k8s_object_name),
                            "status_code":0,
                            "data":k8s_objects
                        }
                    )
                return JsonResponse(response_data)                
        else:
            return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.exception("Error in delete_cluster_api \n{}".format(e))
        data =json.loads(request.body.decode("utf-8"))
        response_data={
                            "message":"EXCEPTION IN DELETE KUBERNETES CLUSTER OBJECTS",
                            "status_code":1,
                            "data":[],
                            "cluster_name":"{}".format(data["cluster_name"]),
                            "action":"{}".format(data["action"])
                        }
                    
        return JsonResponse(response_data)            
    

@csrf_exempt
def update_cluster_api(request):
    """
    Request_obj
            {
                "cluster_name":"demo",
                "action":"update-deployment",
                "user_name": "monkey_d_luffy",
                "metadata":{
                    "namespace":"default",
                    "manifest" : "gtdZWxzOgogICAgICAgIGFwcDogbmdpbngtdGVzdHR0",
                    "k8s_object_name":""
                }
            }       
    Response_obj
        {
            "cluster_name": "demo",
            "action": "update-deployment",
            "message": " UPDATE KUBERNETES CLUSTER OBJECT",
            "status_code": 0,
            "data": []
        }
    """    
    try:
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))

            _temp_request_obj ={}
            _temp_request_obj.update(data)

            cluster_name=data["cluster_name"]

            manifest=data["metadata"]["manifest"]
            yaml_data=base64.b64decode(manifest).decode('utf-8')
            yaml_body=yaml.safe_load(yaml_data)

            k8s_object_name=data["metadata"]["k8s_object_name"]
            namespace=data["metadata"]["namespace"]

            api_function=UPDATE_ACTIONS_JSON[data["action"]]
            cluster_details=get_cluster_details(cluster_name=cluster_name)

            response_data={
                "cluster_name":"{}".format(cluster_name),
                "action":"{}".format(data["action"])  
            }
            if len(cluster_details) == 0:
                response_data.update(
                    {
                        "message":"{}".format(PLATFORM_STATE[3404]),
                        "status_code":3404,
                        "data":[]
                    }
                )
                return JsonResponse(response_data)
            else:
                k8s_objects=api_function(   cluster_details,
                                            k8s_object_name=k8s_object_name,
                                            yaml_body=yaml_body,
                                            namespace=namespace
                                        )
                response_data.update(
                        {
                            "message":"UPDATE KUBERNETES CLUSTER OBJECTS {}".format(k8s_object_name),
                            "status_code":0,
                            "data":k8s_objects
                        }
                    )
                return JsonResponse(response_data)
        else:
            return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.exception("Error in update_cluster_api \n{}".format(e))
        data =json.loads(request.body.decode("utf-8"))
        response_data={
                            "message":"EXCEPTION IN UPDATE KUBERNETES CLUSTER OBJECTS",
                            "status_code":1,
                            "data":[],
                            "cluster_name":"{}".format(data["cluster_name"]),
                            "action":"{}".format(data["action"])
                        }
                    
        return JsonResponse(response_data) 
