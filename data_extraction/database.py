from pymongo import MongoClient

# mongo cmd executable here
# "C:\Program Files\MongoDB\Server\4.0\bin\mongo.exe"

# add parameterized database names to extend this across projects


def connect_mongo():

	client = MongoClient('mongodb://localhost:27017')

	db = client.sportSnapshot

	games = db.games

	return games


def insert_into_db(documents):

	games = connect_mongo()

	results = games.insert_many(documents)

	add_count = 0

	for object_id in results.inserted_ids:
		add_count += 1

	print(f'----{add_count} documents added')


def clear_out_db():

	games = connect_mongo()

	x = games.delete_many({})

	print(f'----{x.deleted_count} documents deleted')