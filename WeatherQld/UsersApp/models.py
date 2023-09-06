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
collection = dbname['Users']

#################################


# Create your models here.


def getUsers():

    try:
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def insertUsers(newrecords):
    try:
        
        data_to_insert = []

        for record in newrecords:
            record["Date Created"] = datetime.strptime(record["Date Created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            record["Last Login"] = datetime.strptime(record["Last Login"], "%Y-%m-%dT%H:%M:%S.%f%z")
            data_to_insert.append(record)
        
        data = collection.insert_many(data_to_insert)
        num_records = len(data.inserted_ids)
        return {"message": f"{num_records} record(s) inserted successfully"}

    except Exception as e:
        return {"error": str(e)}


def updateUsers(accessRole, startDate, endDate):
    try:
        #setting the date range to be searched
        start_date = datetime.strptime(startDate, "%d-%m-%Y")
        end_date = datetime.strptime(endDate, "%d-%m-%Y")

        query = {
            "Date Created": {"$gte": start_date, "$lte": end_date}
        }
        update_query = {
            "$set": {"Access Role": accessRole}
        }

        data = collection.update_many(query, update_query)
        num_records = data.modified_count
        return {"message": f"{num_records} record(s) updated successfully"}

    except Exception as e:
        return {"error": str(e)}    
    


def putUsers(recordIDs, newrecords):
    try:
        deleted_ids = []
        
        for record_id in recordIDs:
            try:
                object_id = ObjectId(record_id)
                delete_result = collection.delete_one({"_id": object_id})
                if delete_result.deleted_count > 0:
                    deleted_ids.append(str(object_id))

            except ObjectId.InvalidId:
                pass  # Ignore invalid ObjectId values
        
        
        data_to_insert = []
        for record in newrecords:
            record["Date Created"] = datetime.strptime(record["Date Created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            record["Last Login"] = datetime.strptime(record["Last Login"], "%Y-%m-%dT%H:%M:%S.%f%z")
            data_to_insert.append(record)

        data = collection.insert_many(data_to_insert)

        num_records_deleted = len(deleted_ids)
        num_records_inserted = len(data.inserted_ids)

        return {
            "message": f"{num_records_deleted} record(s) deleted successfully and {num_records_inserted} record(s) inserted successfully",
            "deleted_ids": deleted_ids
        }

    except Exception as e:
        return {"error": str(e)}


def deleteUsers():
    try:
        #get current date
        current_date = datetime.now()    

        #identify old date based on the 30 days
        old_date = current_date - relativedelta(days=30)

        # in place of a tringger when existing users are inactive for 30 days not including admin users
        query = {
            "Last Login": {"$lt": old_date},
            "Access Role": {"$ne": "Admin"}
        }

        data = collection.delete_many(query)

        num_records_deleted = data.deleted_count
        return {"message": f"{num_records_deleted} record(s) deleted successfully"}

    except Exception as e:
        return {"error": str(e)}


def deleteUserID(ID):
    try:
        query = {"_id": ObjectId(ID)}
        result = collection.delete_one(query)
        
        if result.deleted_count == 0:
            return {"message": "No record found for deletion"}
            
        else:
            return {"message": "Record deleted successfully"}

    except Exception as e:
        return {"error": str(e)}


#def getMeteoritesLimit(p):
#    cursor = collection.find().limit(p)
#    list_cur = list(cursor)
#    json_data = dumps(list_cur)
#    print("JSON Data" + json_data)
#    return json_data
