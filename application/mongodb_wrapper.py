from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBWrapper:
    def __init__(self, mongodb_cfg):
        uri = mongodb_cfg['URI']
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        self.database = self.client[mongodb_cfg['Database']]

    def insert_one(self, collection_name, document):
        collection = self.database[collection_name]
        collection.insert_one(document)

    def find_documents(self, collection_name, query=None, data=None):
        if data is None: data = {}
        collection = self.database[collection_name]
        if query is None:
            return list(collection.find({}, {}))
        return list(collection.find(query, data))

    def update_document(self, collection_name, query, update_data):
        collection = self.database[collection_name]
        collection.update_one(query, {'$set': update_data})

    def delete_document(self, collection_name, query):
        collection = self.database[collection_name]
        collection.delete_one(query)

    def close_connection(self):
        self.client.close()
