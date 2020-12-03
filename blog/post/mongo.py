from pathlib import Path
import pymongo
import json, traceback
from datetime import datetime
from bson.objectid import ObjectId
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING!!
with open("key.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# mongo db connect pool
def search_objectid(object_id):
    try:
        client = pymongo.MongoClient(
            host=get_secret('database_host'),
            port=get_secret('database_port'),
            username=get_secret('database_username'),
            password=get_secret('database_password'),
            authSource=get_secret('authSource')
        )
        blog_db = client['{}'.format(get_secret('database_name'))]
        blog_collection = blog_db['{}'.format(get_secret('collection'))]
        print('Mongo DB Connected')

        cursor = blog_collection.find({'_id': ObjectId(object_id)})

        #문자열로 다시 변환
        results = []
        for document in list(cursor):
            document['_id'] = str(document['_id'])
            document['published_date'] = 
            results.append(document)

        results = json.dumps(results[0])
        print(results)
        print(type(results))
        return results
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('Mongo DB Closed')

