from fastapi import FastAPI
from routes.user import user

service_user = FastAPI()

service_user.include_router(user)

# user_dependency = Annotated[dict, Depends(get_current_user)]

# @app.get('/', status_code=status.HTTP_200_OK)
# async def user(user: user_dependency):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Authentication failed')
#     return {'User': user}
