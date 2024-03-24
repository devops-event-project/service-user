import os
from pymongo import MongoClient

db_host = os.getenv("DB_HOST", "mongo")
db_port = os.getenv("DB_PORT", 27017)

# Establish a connection to the MongoDB server
client = MongoClient(f"mongodb://{db_host}:{db_port}")
db = client['calendar_db']
users = db['users']
