from django.db import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps

import pymongo
import urllib




#################################
#Connecting to the Database
#################################

#Connect to MongoDB Atlas...
client = pymongo.MongoClient('mongodb+srv://normyroe:' + urllib.parse.quote('normy@@699') + '@nasadata.atwjufi.mongodb.net/')

#Define Db Name
dbname = client['Weather']

#Define Collection
collection = dbname['Stations']

#################################


# Create your models here.

def getStation():
    try:
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def insertStation(newrecord):
    try:
        data = collection.insert_one(newrecord)
        return {"message": "Record inserted successfully"}

    except Exception as e:
        return {"error": str(e)}


def getStationID(name):
    try:
        cursor = collection.find({"Station Name": name},{"_id"})
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


#def insertStation(newrecord):
#    try:
#        data = collection.insert_one(newrecord)
#        return data
#
#    except Exception as e:
#        return {"error": str(e)}

