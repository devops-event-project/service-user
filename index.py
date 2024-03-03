from fastapi import FastAPI
from routes.userRoutes import user

service_user = FastAPI()

service_user.include_router(user)
