from fastapi import APIRouter

from models.user import User
from config.db import conn
from schemas.user import serializeDict, serializeList
from bson import ObjectId

user = APIRouter()

@user.get('/user/', tags=["Get Methods"])
async def find_all_users():
    return serializeList(conn.local.user.find())

@user.get('/user/{id}', tags=["Get Methods"])
async def fine_one_user(id):
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/user/', tags=["Post Methods"])
async def create_user(user: User): # Which we have created in models
    result = conn.local.user.insert_one(dict(user))
    return serializeDict(conn.local.user.find_one({"_id":result.inserted_id}))

@user.put('/user/{id}', tags=["Put Methods"])
async def update_user(id, user: User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/user/{id}', tags=["Delete Methods"])
async def delete_user(id):
    return serializeDict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))
