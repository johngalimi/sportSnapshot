from pymongo import MongoClient

# mongo cmd executable here
# "C:\Program Files\MongoDB\Server\4.0\bin\mongo.exe"


def connect_mongo(collection_name, database_name):

    print("---->> Connecting to Mongo")

    client = MongoClient("mongodb://localhost:27017")

    collection = client[collection_name]

    database = collection[database_name]

    return client, database


def insert_into_db(database, documents):

    print("---->> Inserting into Mongo")

    results = database.insert_many(documents)

    add_count = 0

    for object_id in results.inserted_ids:
        add_count += 1

    print(f"--> {add_count} documents added")


def clear_out_db(database):

    "---->> Deleting from Mongo"

    x = database.delete_many({})

    print(f"--> {x.deleted_count} documents deleted")


def close_mongo(client):

    print("---->> Closing Mongo")

    client.close()
