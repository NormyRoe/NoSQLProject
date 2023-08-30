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
            json_data = models.getReadings()
            return JsonResponse(json_data, safe=False)

        except Exception as e:
            return error_response(str(e), status_code=500)

    
    if (request.method == "POST"):
        try:
            body = json.loads(request.body.decode("utf-8"))

            required_fields = ['records']

            for field in required_fields:
                if field not in body:
                    return error_response(f"Missing '{field}' in request body", status_code=400) 
            
            newrecords = body['records']
            response = models.insertReadings(newrecords)
            return JsonResponse(response, status=201, safe=False)

        except Exception as e:
            return error_response(str(e), status_code=500)

    
    if (request.method == "PATCH"):
        try:
            body = json.loads(request.body.decode("utf-8"))
            
            readingID = body['_id']
            precipitationValue = body['Precipitation mm/h']
                    
            response = models.updatePrecipitation(readingID, precipitationValue)
            return JsonResponse(response, status=201, safe=False)

        except Exception as e:
            return error_response(str(e), status_code=500)



def error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)


