from pymongo import MongoClient

# mongo cmd executable here
# "C:\Program Files\MongoDB\Server\4.0\bin\mongo.exe"


def connect_mongo():

	client = MongoClient('mongodb://localhost:27017')

	db = client.sportSnapshot

	games = db.games

	return games


def insert_into_db(documents):

	games = connect_mongo()

	results = games.insert_many(documents)

	for object_id in results.inserted_ids:

		print(f'Game Added, Game ID = {object_id}')


def clear_out_db():

	games = connect_mongo()

	x = games.delete_many({})

	print(x.deleted_count, " documents deleted.")

