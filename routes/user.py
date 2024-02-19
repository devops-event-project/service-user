from datetime import timedelta, datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from config.db import conn
from models.user import User, UserToken
from schemas.user import serializeDict, serializeList
from pytz import timezone

user = APIRouter(prefix='/user')

SECRET_KEY = 'zd%t00xw9-&h1#shs$aqguplrc=$x@3jlh1_kwtd7u8z!@i$ym'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 20

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/auth/token')

# --- Private Methods ---------------------------------------------------------
def authenticate_user(username: str, password: str):
    user = conn.local.user.find_one({'username':username})
    print("-----------")
    print("-----------")
    print(user)
    print("-----------")
    if not user:
        return False
    if not bcrypt_context.verify(password, user['password']):
        return False
    return user    

def create_access_token(username: str, id: ObjectId, expires_delta: timedelta):
    encode = {'sub': username, 'id': str(id)}
    amsterdam_tz = timezone('Europe/Amsterdam')
    expires = datetime.now(amsterdam_tz) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id: str = payload.get('id')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')

# --- API Methods -------------------------------------------------------------
@user.get('/', tags=["Get Methods"])
async def find_all_users(user: User = Depends(get_current_user)):
    return serializeList(conn.local.user.find())

@user.get('/{id}', tags=["Get Methods"])
async def fine_one_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/auth/register', tags=["Post Methods"])
async def register(user: User): # Which we have created in models
    new_user = User(
        username = user.username,
        email = user.email,
        password = bcrypt_context.hash(user.password)
    )
    result = conn.local.user.insert_one(dict(new_user))
    return serializeDict(conn.local.user.find_one({"_id":result.inserted_id}))

@user.post('/auth/token', tags=["Post Methods"], response_model=UserToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    token = create_access_token(user['username'], user['_id'], expires)

    return {
        'access_token': token, 
        'token_type': 'bearer'
    }

@user.put('/{id}', tags=["Put Methods"])
async def update_user(id: str, user: User = Depends(get_current_user)):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}', tags=["Delete Methods"])
async def delete_user(id: str, user: User = Depends(get_current_user)):
    return serializeDict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))