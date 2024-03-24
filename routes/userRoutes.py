from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta
from bson import ObjectId

from config.database.connection import users
from config.security.auth import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRES_MINUTES
from models.userModel import User
from controller.userController import create_user, authenticate_user
from schemas.userSchemas import UserToken, serializeDict, serializeList

# Creating a router for user endpoints
user = APIRouter(prefix='/user')

# Endpoint to retrieve all users. Requires that the requestor is an authenticated user.
@user.get('/', tags=["Get Methods"])
async def find_all_users(user: User = Depends(get_current_user)):
    return serializeList(users.find())

# Endpoint to retrieve a single user by their ID. Requires user authentication.
@user.get('/{id}', tags=["Get Methods"])
async def fine_one_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(users.find_one({"_id":ObjectId(id)}))

# Endpoint for user registration. Accepts a User model and creates a new user in the database.
@user.post('/register', tags=["Post Methods"])
async def register(user: User):
    user = create_user(user)
    return serializeDict(users.find_one({"_id":user.inserted_id}))

# Endpoint for user login. Uses form data for authentication and, if successful, returns a bearer token.
@user.post('/login', tags=["Post Methods"], response_model=UserToken)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    
    # Set token expiration time
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRES_MINUTES)
    user_data = {
        'sub': user['username'], 
        'id': str(user['_id'])
    }
    # Create access token
    access_token = create_access_token(user_data, access_token_expires)

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    print('hey')
    return {
        'access_token': access_token, 
        'token_type': 'bearer'
    }

# Endpoint to update a user's information by their ID. Requires user authentication.
@user.put('/{id}', tags=["Put Methods"])
async def update_user(id: str, user: User = Depends(get_current_user)):
    users.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return serializeDict(users.find_one({"_id":ObjectId(id)}))

# Endpoint to delete a user by their ID. Requires user authentication.
@user.delete('/{id}', tags=["Delete Methods"])
async def delete_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(users.find_one_and_delete({"_id":ObjectId(id)}))