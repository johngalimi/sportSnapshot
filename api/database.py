from pymongo import MongoClient

# mongo cmd executable here
# "C:\Program Files\MongoDB\Server\4.0\bin\mongo.exe"

# should centralize all database operations in one folder (crawl / api agnostic)


def connect_mongo(collection_name, database_name):

	print('---->> Connecting to Mongo')

	client = MongoClient('mongodb://localhost:27017')

	collection = client[collection_name]

	database = collection[database_name]

	return client, database


def close_mongo(client):

	print('---->> Closing Mongo')

	client.close()


