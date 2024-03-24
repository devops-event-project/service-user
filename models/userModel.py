from pydantic import BaseModel

# Model for User event
class User(BaseModel):
    email: str
    username: str
    password: str
    is_admin: bool

    
