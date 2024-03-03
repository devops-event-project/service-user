from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta
from bson import ObjectId

from config.database.connection import db
from config.security.auth import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRES_MINUTES
from models.userModel import User
from controller.userController import create_user, authenticate_user
from schemas.userSchemas import UserToken, serializeDict, serializeList


user = APIRouter(prefix='/user')

@user.get('/', tags=["Get Methods"])
async def find_all_users(user: User = Depends(get_current_user)):
    return serializeList(db.local.user.find())

@user.get('/{id}', tags=["Get Methods"])
async def fine_one_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(db.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/register', tags=["Post Methods"])
async def register(user: User):
    user = create_user(user)
    return serializeDict(db.local.user.find_one({"_id":user.inserted_id}))

@user.post('/login', tags=["Post Methods"], response_model=UserToken)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRES_MINUTES)
    user_data = {
        'sub': user['username'], 
        'id': str(user['_id'])
    }
    access_token = create_access_token(user_data, access_token_expires)

    response.set_cookie(key="accesss_token", value=access_token, httponly=True)
    return {
        'access_token': access_token, 
        'token_type': 'bearer'
    }

@user.put('/{id}', tags=["Put Methods"])
async def update_user(id: str, user: User = Depends(get_current_user)):
    db.local.user.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return serializeDict(db.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}', tags=["Delete Methods"])
async def delete_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(db.local.user.find_one_and_delete({"_id":ObjectId(id)}))