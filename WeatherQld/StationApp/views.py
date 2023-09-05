from . import models
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps

import pymongo

from django.http import Http404


# Create your views here.

def TheModelView(request):
    if (request.method == "GET"):
        try:
            json_data = models.getStation()
            return JsonResponse(json_data, safe=False)

        except Exception as e:
            return error_response(str(e), status_code=500)

    
    if (request.method == "POST"):
        try:
            body = json.loads(request.body.decode("utf-8"))

            required_fields = ['stationName', 'address', 'sensorName', 'longitude', 'latitude', 'access role']

            for field in required_fields:
                if field not in body:
                    return error_response(f"Missing '{field}' in request body", status_code=400) 
            
            access_role = body['access role']

            newrecord = {
                "Station Name": body['stationName'],
                "Station Address": body['address'],
                "Sensor": body['sensorName'],                
                "Longitude": body['longitude'],
                "Latitude": body["latitude"]                       
            }
            
            if (access_role == "Admin"):
                response = models.insertStation(newrecord)
                return JsonResponse(response, status=201, safe=False)

            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)


def StationID(request, name):
    if (request.method == "GET"):
        try:
            json_data = models.getStationID(name)

            if (json_data == "[]"):
                #raise Http404
                return HttpResponse("Document not found", status=404)

            else:
                return JsonResponse(json_data, safe=False)
        
        except Exception as e:
            return error_response(str(e), status_code=500)


def error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)


#if (request.method == "POST"):
#        try:
#            body = json.loads(request.body.decode("utf-8"))        
#            
#            newrecord = {
#                "Station Name": body['stationName'],
#                "Station Address": body['address'],
#                "Sensor": body['sensorName'],                
#                "Longitude": body['longitude'],
#                "Latitude": body["latitude"]                       
#            }
#            
#            response = models.insertStation(newrecord)
#            return JsonResponse(response, safe=False)
#
#        except Exception as e:
#            return error_response(str(e), status_code=500)