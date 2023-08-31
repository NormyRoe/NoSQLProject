from django.db import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from bson.json_util import dumps

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

collection2 = dbname['Stations']
#################################


# Create your models here.


def getReadings():
    try:
        cursor = collection.find().batch_size(batch_size).limit(100)
        readings = list(cursor)
        json_data = dumps(readings)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def getMaximumPrecipitation(sensor, duration, agrrfunc):
    try:
        #get current date
        current_date = datetime.now()

        #specify an integer variable for duration
        int_duration = int(duration)

        #identify old date based on the duration amount
        old_date = current_date - relativedelta(months=int_duration)
        

        #set query
        query = {
            "Device Name": sensor,
            "Time": {
                "$gte": old_date,
                "$lt": current_date
            }
        }

        #set projection
        projection = {
            "_id",
            "Device Name",
            "Time",
            "Precipitation mm/h"
        }

        #set sort order
        #this gets the Max value by sorting in descending order and
        #retrieving the first record
        sort_order = [("Precipitation mm/h", -1)]


        cursor = collection.find(query, projection).sort(sort_order).limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def parse_sensor_string(sensor_string):
    try:
        # Remove leading and trailing square brackets and newlines
        sensor_string = sensor_string.strip()[1:-1].replace("\n", "")

        # Split by curly braces to get individual sensor entries
        sensor_entries = sensor_string.split("{")

        sensor_list = []
        for entry in sensor_entries:
            if "Device Name" in entry:
                device_name = entry.split(":")[1].split("}")[0].strip().strip("\"")
                sensor_list.append(device_name)

        return sensor_list

    except Exception as e:
        return {"error": str(e)}


def getSensors(station):
    try:
        #set query
        query = {
            "Station Name": station
        }
        
        cursor = collection2.find(query)
        list_cur = list(cursor)

        # Parse the "Sensor" field and extract "Device Name" values
        device_names = []
        for item in list_cur:
            sensor_list = parse_sensor_string(item["Sensor"])
            device_names.extend(sensor_list)


        print("list_cur Data" + str(list_cur))
        
        return device_names

    except Exception as e:
        return {"error": str(e)}


def getStationSensorReadings(device_names, date):
    try:

        #setting the date to be searched
        start_date = datetime.strptime(date, "%d-%m-%Y %H:%M")
        end_date = start_date + relativedelta(hours=1)

        #set query
        query = {
            "Device Name": {"$in": device_names},
            "Time": {
            "$gte": start_date,
            "$lt": end_date
            } 
        }

        #set projection
        projection = {        
            "Temperature (°C)",
            "Atmospheric Pressure (kPa)",
            "Solar Radiation (W/m2)",
            "Precipitation mm/h"
        }

        cursor = collection.find(query, projection)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}


def getMaximumTemperature(startDate, endDate, agrrfunc):
    try:
    
        #setting the date to be searched
        start_date = datetime.strptime(startDate, "%d-%m-%Y")
        end_date = datetime.strptime(endDate, "%d-%m-%Y")    
        

        #set query
        query = {
            "Time": {
                "$gte": start_date,
                "$lte": end_date
            }
        }

        #set projection
        projection = {
            "_id",
            "Device Name",
            "Time",
            "Temperature (°C)"
        }

        #set sort order
        #this gets the Max value by sorting in descending order and
        #retrieving the first record
        sort_order = [("Temperature (°C)", -1)]


        cursor = collection.find(query, projection).sort(sort_order).limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("JSON Data" + json_data)
        return json_data

    except Exception as e:
        return {"error": str(e)}
