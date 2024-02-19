from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str

    
