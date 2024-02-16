def userEntity(item) -> dict:
	return {
		"id":str(item["_id"]),
		"name":str(item["name"]),
		"email":str(item["email"]),
		"password":str(item["password"]),

	}

def usersEntity(items) -> list:
	return [userEntity(item) for item in items]

def serializeDict(item) -> dict:
	return {**{i:str(item[i]) for i in item if i=='_id'},**{i:item[i] for i in item if i!='_id'}}

def serializeList(items) -> list:
	return [serializeDict(item) for item in items]