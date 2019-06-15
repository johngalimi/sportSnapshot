from pymongo import MongoClient

# put mongo cmd  executable here

def insert_into_db(documents):

	client = MongoClient('mongodb://localhost:27017')

	db = client.sportSnapshot

	games = db.games

	results = games.insert_many(documents)

	for object_id in results.inserted_ids:

		print(f'Game Added, Game ID = {object_id}')


def clear_out_db():

	x = games.delete_many({})

	print(x.deleted_count, " documents deleted.")

