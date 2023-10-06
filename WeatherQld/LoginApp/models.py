from django.db import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps
from bson import ObjectId
from bson.objectid import ObjectId

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
collection = dbname['Users']

#################################


# Create your models here.

def getLogin(username, password):

    try:

        #set query
        query = {
            "Username": username,
            "Password": password
        }

        #set projection
        projection = {
            "_id": 0,
            "Access Role": 1
        }

        cursor = collection.find(query, projection)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


