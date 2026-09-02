import sqlalchemy

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request

from sqlmodel import select

from app.core.session import SessionDep
from app.models.users_model import UsersCreate, Users
from app.services import users_service

import app.repo.users_repo as user_repo

app = FastAPI()
router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
async def create_user(user: UsersCreate, session: SessionDep, request: Request):
    user = Users.model_validate(user)
    user = users_service.hash_password_user(user)
    
    return user_repo.add_user_to_db(user, session)

@router.get("/{user_id}")
async def check_user(user_id: int, session: SessionDep):
    return users_service.return_all_users_or_one(user_id, session)


app.include_router(router)
