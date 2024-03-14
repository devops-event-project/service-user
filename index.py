from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoutes import user

service_user = FastAPI()

service_user.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service_user.include_router(user)
