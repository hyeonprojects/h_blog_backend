from pathlib import Path
from bson.objectid import ObjectId
from django.core.exceptions import ImproperlyConfigured
from pymongo import MongoClient

import json, traceback, os

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

# todo : setting 파일데이터를 가져오는 듯, 중복을 최소화 하면 좋겠지만

class MongoDbManager:
    def __init__(self):
        self.host = get_secret('database_host')
        self.port = get_secret('database_port')
        self.username = get_secret('database_username')
        self.password = get_secret('database_password')
        self.authSource = get_secret('authSource')
        self.client = None
        self.database = None
        self.database = None

    def connection(self):
        self.client = MongoClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            authSource=self.authSource
        )
        self.database = self.client['{}'.format(get_secret('database_name'))]['{}'.format(get_secret('collection'))]
        print('Mongo Db Connected')

        if self.database == None:
            assert print(traceback.format_exc())

    def close(self):
        self.client.close()
        print('Mongo Db Close')

    def post_read(self, id):
        """
        Post 내용을 id를 통해서 가져오는 함수
        """
        # 데이터를 가져오는거에요.
        cursor = self.database.find({'_id': ObjectId(id)})
        # _id를 str -> ObjectId로 전환, published_date를 str -> datetime으로 전환
        result = []
        for document in list(cursor):
            document['_id'] = str(document['_id'])
            document['published_date'] = str(document['published_date'])
            result.append(document)
        self.close()
        return result

    def post_update(self, id, data):
        """
        Post 내용을 post를 통해서 데이터를 찾고 그 일부분을 바꾸는거.
        """
        database_data = self.post_read(id)[0]
        database_data['title'] = data['title']
        database_data['body'] = data['body']
        database_data['tags'] = data['tags']
        del database_data['_id']

        self.database.find_one_and_replace(
            {'_id': ObjectId(id)}, database_data,
            projection={'_id':False,'published_date':False}
        )
        self.close()
        return database_data

    def post_delete(self, id):
        """
        Post 내용을 id를 통해서 삭제하는 함수
        """
        result = self.database.delete_one({'_id': ObjectId(id)})
        self.close()
        return print('{}개 삭제되었습니다.'.format(result.deleted_count))
