from fastapi import FastAPI

app = FastAPI()

from app.api.routers.users import router as user_router
from app.api.routers.auth import router as auth_router

app.include_router(user_router)
app.include_router(auth_router)
