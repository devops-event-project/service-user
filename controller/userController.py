from models.userModel import User
from config.security.auth import verify_password, pwd_context
from config.database.connection import users

def create_user(user: User):
    """
    Creates a new user in the database.

    Parameters:
    - user (User): An instance of the User model containing the new user's information.

    The function hashes the user's password before saving the user to the database.

    Returns:
    - The result of the MongoDB insert operation if successful; False otherwise.
    """
    # Hashing the password using the password context
    new_user = User(
        username = user.username,
        email = user.email,
        password = pwd_context.hash(user.password),
        is_admin = user.is_admin
    )

    try:
        # Attempting to insert the new user into the database
        new_user = users.insert_one(dict(new_user))
    except:
        # Returning False if the insert operation fails
        return False
    return new_user
    
def get_user_by_username(username: str):
    # Finding the user in the database by username and return the result
    return users.find_one({'username':username})

def authenticate_user(username: str, password: str):
    """
    Authenticates a user by their username and password.

    Parameters:
    - username (str): The username of the user to authenticate.
    - password (str): The password provided by the user for authentication.

    Returns:
    - The user's document from the database if authentication is successful; False otherwise.
    """
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    # Returning the user document if authentication is successful
    return user 