from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import string
import random

# Create your views here.

def get(request):
    mongo_client = MongoClient("localhost",27017)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    cursor = mongo_collection.find({})
    #l = list(cursor)
    #return JsonResponse({"status": 200,"message":json.dumps(l)})
    import json
    from bson.json_util import dumps
    return JsonResponse({"status": 200,"message":json.loads(dumps(cursor))})   
    #return JsonResponse(json.dumps(list(cursor)))

def put(request):
    mongo_client = MongoClient("localhost",27017)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    all_data = {}
    all_data['create_date'] = datetime.now()
    all_data['message'] = id_generator(100)
    mongo_result = mongo_collection.insert(all_data)

    return JsonResponse({"status": 200,
                         "message": str(mongo_result)})
                         
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):    
    return ''.join(random.choice(chars) for _ in range(size))