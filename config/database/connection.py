import os
from pymongo import MongoClient

db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 27017)

print(f"mongodb://{db_host}:{db_port}")

client = MongoClient(f"mongodb://{db_host}:{db_port}")
db = client['calendar_db']
users = db['users']

