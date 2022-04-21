import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .mail import email

@csrf_exempt
def send_email(request):
    print("content in http request: \n{}".format(request))
    data =json.loads(request.body.decode("utf-8"))
    print("content in http request: \n{}".format(data))

    try: 
        if request.method == 'POST':
            username=data["username"]
            gmail=data["gmail"]
            emailsending = email(username,gmail)
            
            return JsonResponse({"message":"email successfully send "})

        return JsonResponse({"message":"Invalid http request"})
    except Exception as e:
        print("Error in views--> send_email\n{}".format(e))
        return JsonResponse({"message":"EMail sending failed"})