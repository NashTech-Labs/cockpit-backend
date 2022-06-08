from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .platform_utils import *
from .serializers import *
from user.serializers import *
from .platform_state import PLATFORM_STATE

import logging

#Get an instance of a specific named logger
logger = logging.getLogger('platform-view')


# Create your views here.
@csrf_exempt
def create_platform_request(request):

    """{
            "user_name":"sachinvd",
            "user_email":"sachinvd@gmail.com",
            "platform":"jenkins",
            "project_details":{
                "git_url":"",
                "git_branch":"",
                "git_token":"",
                "docker_reponame":"",
                "docker_tag":"",
                "docker_registry_url":"",
                "docker_username":"",
                "docker_password":"",
                "docker_file_path":"",
                "docker_build_context":"",
                "language":"",
                "version":"",
                "framework":""
            }
        }
    """
    try:
        if request.method == 'POST':
            data =json.loads(request.body.decode("utf-8"))

            _temp_request_obj ={}
            _temp_request_obj.update(data)

            create_user_entry_in_db(data)
            create_project_details_entry_in_db(data)

            logger.info("user-details {}".format(data))

            create_platform.delay(data)

            state={
                "platform_state":1000,
                "message": "{}".format(PLATFORM_STATE[1000])
            }
            data.update(state)

            return JsonResponse(data)
        return JsonResponse({"message":"invalid request {}".format(request.method)})
    except Exception as e:
        logger.error("Error in platform view request {}".format(e))       
        return JsonResponse(JsonResponse(data.update({"platform_state":999})))
        #return JsonResponse(data.update({"platform_state":999}))