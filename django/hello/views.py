from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import string
import random
import multiprocessing

# Create your views here.
configData = 'mongodb://mongo:27017'
def get(request):
    mongo_client = MongoClient(configData)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    total = mongo_collection.count({})
    # import json
    # from bson.json_util import dumps
    return JsonResponse({"status": 200,"total":total})
    #return JsonResponse(json.dumps(list(cursor)))

def put(request):
    mongo_client = MongoClient(configData)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    all_data = {}
    all_data['create_date'] = datetime.now()
    all_data['message'] = id_generator(100)
    all_data['message2'] = id_generator(100)
    all_data['message3'] = id_generator(100)
    all_data['message4'] = id_generator(100)
    mongo_result = mongo_collection.insert(all_data)
    all_data['create_date'] = str(all_data['create_date'])
    return JsonResponse({"status": 200,
                         "data": {
                             "id" : str(mongo_result),
                             "message" : all_data['message'],
                             "message2" : all_data['message2'],
                             "message3" : all_data['message3'],
                             "message4" : all_data['message4'],
                         }})

def query(request):
    message = request.GET.get('message')
    mongo_client = MongoClient(configData)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    query = {"$regex" : ".*"+message+".*"}
    result =  mongo_collection.find({ "$or": [{"message":query},{"message2":query},{"message3":query},{"message4":query}] }).limit(10)
    import json
    from bson.json_util import dumps
    if result is None:
        result = []
    return JsonResponse({"status": 200,
                         "data": json.loads(dumps(result))})

#generate default data for testing that reach to 250MB for mongo data size
def init(number):
    mongo_client = MongoClient(configData)
    mongo_db = mongo_client.database
    mongo_collection = mongo_db.log
    for i in range(number):
        all_data = {}
        all_data['create_date'] = datetime.now()
        all_data['message'] = id_generator(100)
        all_data['message2'] = id_generator(100)
        all_data['message3'] = id_generator(100)
        all_data['message4'] = id_generator(100)
        mongo_collection.insert(all_data)

    return True


def initData(request,number = 2000000):
    number = int(number)
    if number ==0:
        number = 2000000

    p = multiprocessing.Process(target=init,args=(number,))
    p.daemon = True
    p.start()
    return JsonResponse({"status": 200,
                         "message": "Init default data processing. Number: "+str(number)})
                         
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):    
    return ''.join(random.choice(chars) for _ in range(size))