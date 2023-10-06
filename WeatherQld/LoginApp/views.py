from . import models
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps

import pymongo


# Create your views here.

def TheModelView(request):
    if (request.method == "GET"):

        try:            
            body = json.loads(request.body.decode("utf-8"))

            required_fields = ['username', 'password']

            for field in required_fields:
                if field not in body:
                    return error_response(f"Missing '{field}' in request body", status_code=400) 
            

            username = body['username']
            password = body['password']

            json_data = models.getLogin(username, password)

            if (json_data == "[]"):
                #raise Http404
                return HttpResponse("User not found", status=404)

            else:                
                return JsonResponse(json_data, safe=False)
            

        except Exception as e:
            return error_response(str(e), status_code=500)


def error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)