from pydantic import BaseModel

"""
Defines data models for Users
"""


# Model for User event
class User(BaseModel):
    email: str
    username: str
    password: str
    is_admin: bool
