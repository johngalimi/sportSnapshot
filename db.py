from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client.sportSnapshot

games = db.games

