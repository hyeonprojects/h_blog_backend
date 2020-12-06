from pathlib import Path
from bson.objectid import ObjectId
from django.core.exceptions import ImproperlyConfigured
from djongo import models

import json, traceback, os, pymongo

BASE_DIR = Path(__file__).resolve().parent.parent

print(os.getcwd())

# SECURITY WARNING!!
with open('key.json') as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# todo : setting 파일의 데이터를 불러와서 수정하게 제작핳는 것잉 유용함.
# todo : 데코레이터로 만든 이 부분을 수정하기.. try cachl
# connetion 데코레이터!
def connection(func):
    def decorator(*args, **kwargs):
        global blog_collection
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
            func(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            client.close()
            print('Mongo DB Closed')


@connection
def search_post(id):
    """
    Post 내용 물의 값을 mongodb의 _id를 통해서 찾아오는 기능이다.
    """
    # 데이터를 가져오는거에요.
    cursor = blog_collection.find({'_id': ObjectId(id)})
    # _id를 str -> ObjectId로 전환, published_date를 str -> datetime으로 전환
    result = []
    for document in list(cursor):
        document['_id'] = str(document['_id'])
        document['published_date'] = str(document['published_date'])
        result.append(document)
    return result


@connection
def update_post(posts, post_data):
    """
    mongo db Post 데이터를 넣어준다.
    """
    blog_collection.update(posts, post_data, upsert=True)


@connection
def delete_post(id):
    """
    mongo db 파일을 만들어 보았습니다.
    """
    blog_collection.remove({"_id": ObjectId(id)})
