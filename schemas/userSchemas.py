from pydantic import BaseModel

class UserToken(BaseModel):
    access_token: str
    token_type: str

def serializeDict(item) -> dict:
	return {**{i:str(item[i]) for i in item if i=='_id'},**{i:item[i] for i in item if i!='_id'}}

def serializeList(items) -> list:
	return [serializeDict(item) for item in items]