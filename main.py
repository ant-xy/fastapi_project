from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
import sqlalchemy
from sqlmodel import select

from models.users import UsersBase, Users, UsersCreate, UsersRead, Payload, UserLogin, Token
from core.session import SessionDep

from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.bcrypt import BcryptHasher

from datetime import datetime, timedelta, timezone
import jwt

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

password_hash = PasswordHash((BcryptHasher(),))

app = FastAPI()

@app.post("/user/")
async def create_user(user: UsersCreate, session: SessionDep):
    user = Users.model_validate(user)
    print(user.password)
    user.password = password_hash.hash(user.password)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except sqlalchemy.exc.IntegrityError as ex:
        return "Something went wrong, try again later"
    return user

@app.get("/user/")
async def check_user(user_id: int, session: SessionDep):
    user = session.get(Users, user_id)

    if not user:
        all_users = session.exec(select(Users)).all()
        payload = Payload(status=200, message="success", data=all_users)
        return payload

    payload = Payload(status=200, message="success", data=user)
    return payload

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

random_key = "$2b$12$jySqAint0uiSid0g5/1Fgul396tGSlkrNbVHDEZ6DjTJrOtI3XjMy"

@app.post("/login")
async def login_user(detail: UserLogin, session: SessionDep):
    user = session.exec(select(Users).where(Users.username == detail.username)).first()

    if user and password_hash.verify(detail.password, user.password):
        token_jwt = create_access_token({"user": user.username}, expires_delta=timedelta(days=3))
        token = Token(jwt=token_jwt, token_type=ALGORITHM)
        return token
    else:
        #prevent timebased attacks
        password_hash.verify(detail.password, random_key)
        token_jwt = create_access_token({"user": "abc"}, expires_delta=timedelta(days=3))
        return "Username or password incorrect."
