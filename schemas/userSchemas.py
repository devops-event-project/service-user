from pydantic import BaseModel

"""
Provides serialization functions to facilitate the data exchange between the 
API service and MongoDB. It includes two functions: serializeDict, which 
converts MongoDB documents to dictionaries with appropriate type handling for 
object IDs and datetime objects.
serializeList, which applies this serialization to a list of documents.
The UserToken class models the response structure for authentication routes.
"""

class UserToken(BaseModel):
    access_token: str
    token_type: str

# Serialize data between API interface and MongoDB
# Seialize dictionary
def serializeDict(item) -> dict:
	return {**{i:str(item[i]) for i in item if i=='_id'},**{i:item[i] for i in item if i!='_id'}}

# Serlialize list of dictionaries
def serializeList(items) -> list:
	return [serializeDict(item) for item in items]