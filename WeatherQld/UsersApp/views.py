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
            json_data = models.getUsers()
            return JsonResponse(json_data, safe=False)

        except Exception as e:
            return error_response(str(e), status_code=500)
        
    

    if (request.method == "POST"):

        try:
            body = json.loads(request.body.decode("utf-8"))
            
            access_role = body['access role']
            
            newrecords = body['records']
            
            if (access_role == "Admin"):
                response = models.insertUsers(newrecords)
                return JsonResponse(response, status=201, safe=False)
            
            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)


    if (request.method == "PUT"):

        try:
            body = json.loads(request.body.decode("utf-8"))

            access_role = body['access role']

            recordIDs = body['recordIds']

            newrecords = body['records']

            if (access_role == "Admin"):
                response = models.putUsers(recordIDs, newrecords)
                return JsonResponse(response, status=201, safe=False)
            
            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)


    if (request.method == "PATCH"):

        try:
            body = json.loads(request.body.decode("utf-8"))
            
            access_role = body['access_role']

            startDate = body['startDate']
            endDate = body['endDate']
            accessRole = body['Access Role']

            if (access_role == "Admin"):
                response = models.updateUsers(accessRole, startDate, endDate)
                return JsonResponse(response, status=201, safe=False)
            
            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)


    if (request.method == "DELETE"):

        try:
            body = json.loads(request.body.decode("utf-8"))

            access_role = body['access role']

            if (access_role == "Admin"):
                response = models.deleteUsers()
                return JsonResponse(response, status=201, safe=False)
            
            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)



def UserID(request, ID):
    if (request.method == "DELETE"):

        try:
            body = json.loads(request.body.decode("utf-8"))

            access_role = body['access role']

            if (access_role == "Admin"):
                response = models.deleteUserID(ID)
                return JsonResponse(response, status=201, safe=False)
            
            else:
                return HttpResponse("You are not authorised to submit this request", status=403)

        except Exception as e:
            return error_response(str(e), status_code=500)


def error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)
            







#def MaxTemperature(request, period=5):
#    if (request.method == "GET"):
#        json_data = models.getMeteoritesLimit(period)
#        return JsonResponse(json_data, safe=False)
