from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError
from pytz import timezone
from datetime import timedelta, datetime

from config.security.cookie import OAuth2PasswordBearerWithCookie

"""
This module integrates security and authentication mechanisms with the FastAPI
utilizing password hashing, JWT token generation and validation, and user authentication.
It defines utility functions for hashing passwords, verifying hashed passwords,
creating JWT access tokens with custom expiration times, and extracting and validating
user information from JWT tokens.
The module employs the Passlib library for secure password handling, the python-jose
library for JWT operations, and a custom OAuth2 bearer class that supports
cookie-based token retrieval.
"""


SECRET_KEY = 'zd%t00xw9-&h1#shs$aqguplrc=$x@3jlh1_kwtd7u8z!@i$ym'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 60
COOKIE_NAME = 'authorization'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearerWithCookie(tokenUrl='user/login')

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expires_delta: timedelta):
    to_encode = user_data.copy()

    amsterdam_tz = timezone('Europe/Amsterdam')
    expires = datetime.now(amsterdam_tz) + expires_delta
    to_encode.update({'exp': expires})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(access_token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id: str = payload.get('id')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')