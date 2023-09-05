from . import models, views
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps

import pymongo

from django.http import Http404

import datetime
from datetime import datetime


# Create your views here.

def TheModelView(request):
    if (request.method == "GET"):
        try:
            #query parameters
            sensor = request.GET.get('sensor')
            duration = request.GET.get('duration')
            agrrfunc = request.GET.get('agrrfunc')
            station = request.GET.get('station')
            date = request.GET.get('date')
            startDate = request.GET.get('startDate') 
            endDate = request.GET.get('endDate')


            if sensor and duration and agrrfunc:
                return views.MaximumPrecipitation(request, sensor, duration, agrrfunc)

            elif station and date:
                return views.StationSensorReadings(request, station, date)

            elif startDate and endDate and agrrfunc:
                return views.MaximumTempValue(request, startDate, endDate, agrrfunc)

            elif not (sensor or station or startDate):
                batch_size = 10
                json_data = models.getReadings(batch_size)
                return JsonResponse(json_data, safe=False)

            else:
                return HttpResponse("Invalid query parameters")
        

        except Exception as e:
            return error_response(str(e), status_code=500)
    


def MaximumPrecipitation(request, sensor: str, duration: int, agrrfunc: str):
    try:
    
        json_data = models.getMaximumPrecipitation(sensor, duration, agrrfunc)
        
        if (json_data == "[]"):
            #raise Http404
            return HttpResponse("Document not found", status=404)

        else:
            return JsonResponse(json_data, safe=False)
    
    except Exception as e:
            return error_response(str(e), status_code=500)
        

def StationSensorReadings(request, station: str, date: datetime):
    try:
    
        device_names = models.getSensors(station)    
        
        new_json_data = models.getStationSensorReadings(device_names, date)

        if (new_json_data == "[]"):
            #raise Http404
            return HttpResponse("Documents not found", status=404)

        else:
            return JsonResponse(new_json_data, safe=False)
    
    except Exception as e:
            return error_response(str(e), status_code=500)


def MaximumTempValue(request, startDate: datetime, endDate: datetime, agrrfunc: str):
    try:
    
        json_data = models.getMaximumTemperature(startDate, endDate, agrrfunc)
        
        if (json_data == "[]"):
            #raise Http404
            return HttpResponse("Document not found", status=404)

        else:
            return JsonResponse(json_data, safe=False)
    
    except Exception as e:
            return error_response(str(e), status_code=500)


def error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)