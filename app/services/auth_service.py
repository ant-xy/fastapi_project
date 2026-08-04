from sqlmodel import select

from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.bcrypt import BcryptHasher

from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from app.models.users_model import Users

from app.schemas.request.users_request import UserLogin, Token
from app.core.session import SessionDep
import app.services.auth_service as auth

password_hasher = PasswordHash((BcryptHasher(),))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def login_user(detail: UserLogin, session: SessionDep):
    user = session.exec(select(Users).where(Users.username == detail.username)).first()
    password_hash = None

    try:
        password_hash = password_hasher.verify(detail.password, user.password)
    except InvalidTokenError, exceptions.UnknownHashError:
        return "Something went wrong!"

    if password_hash and user:
        token_jwt = auth.create_access_token({"user": user.username}, expires_delta=timedelta(days=3))
        token = Token(jwt=token_jwt, token_type="bearer")
        return token
    else:
        return "Username or password incorrect."
