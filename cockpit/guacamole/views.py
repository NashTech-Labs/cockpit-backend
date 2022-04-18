from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.http import HttpResponse, JsonResponse
import json
# Create your views here.
from datetime import datetime
#from .guacamole_utils import get_active_connections_details
from .guacamole_utils import *
from django.views.decorators.csrf import csrf_exempt
import logging

@csrf_exempt
def create_connection(request):
    """Accept request to create Guacamole Connection Sharing Policy
        Example payload:
        {
            'name' : 'something_unique'
            'hostname' : "0.0.0.0",
            'port' : '22',
            'protocol' : 'ssh',
            'username' : 'CrazyMonkey',
            'password' : 'BananaNotAvialableInDeserts',
            'private-key' : ''
        }
    """
    if request.method == 'POST':

        SHARING_PROFILE_URL=""

        data =json.loads(request.body.decode("utf-8"))
        _temp_request_obj ={}
        _temp_request_obj.update(data)

        connection_details=create_guacamole_connection(data)

        if len(connection_details) != 0:

            profile=create_sharing_profile(connection_details)

            print("\n profile :{}".format(profile))

            sharing_profile_id=profile['identifier']

            active_connections_id=get_active_connection_details(connection_details)
            print(" active connections: {} \n sharing_profile_id: {}".format(active_connections_id, sharing_profile_id))
            if active_connections_id is not None:
                #SHARING_PROFILE_URL=get_sharing_profile_url(active_connections_id,sharing_profile_id)
                return JsonResponse({"URL":"{}".format(get_sharing_profile_url(active_connections_id,sharing_profile_id))})
            else:
                return JsonResponse({"URL": None})
        else:
            JsonResponse({"URL": None})
    return  JsonResponse({"message":"invalid http request method {}".format(request.method)})
