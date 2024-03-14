from models.userModel import User
from config.security.auth import verify_password, pwd_context
from config.database.connection import users

def create_user(user: User):
    new_user = User(
        username = user.username,
        email = user.email,
        password = pwd_context.hash(user.password),
        is_admin = user.is_admin
    )

    try:
        new_user = users.insert_one(dict(new_user))
    except:
        return False
    return new_user
    
def get_user_by_username(username: str):
    return users.find_one({'username':username})

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user 