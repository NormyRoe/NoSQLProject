from django.db import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps
from bson import ObjectId

import pymongo
import urllib

import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

#################################
#Connecting to the Database
#################################

#Connect to MongoDB Atlas...
client = pymongo.MongoClient('mongodb+srv://normyroe:' + urllib.parse.quote('normy@@699') + '@nasadata.atwjufi.mongodb.net/')

#Define Db Name
dbname = client['Weather']

#Define Collection
collection = dbname['Readings']

#################################


# Create your models here.


def getReadings():
    try:
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def insertReadings(newrecords):
    try:
        data_to_insert = []

        for record in newrecords:
            record["Time"] = datetime.strptime(record["Time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            data_to_insert.append(record)

        data = collection.insert_many(data_to_insert)
        num_records = len(data.inserted_ids)
        return {"message": f"{num_records} record(s) inserted successfully"}

    except Exception as e:
        return {"error": str(e)}


def updatePrecipitation(readingID, precipitationValue):
    try:

        query = {
                "_id": ObjectId(readingID)
        }
        update_query = {
                "$set": {"Precipitation mm/h": precipitationValue}
        }
        data = collection.update_one(query, update_query)

        if data.matched_count == 1 and data.modified_count == 1:
            return {"message": "Record updated successfully"}

        else:
            return {"message": "Record not found or not updated"}

    except Exception as e:
        return {"error": str(e)}


