from fastapi import APIRouter, HTTPException, status

from app.core.session import SessionDep

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.services import auth_service

from app.schemas.request.users_request import Token, UserLogin


router = APIRouter(tags=["auth"])


@router.post("/token_valid/")
async def validate_jwt(token: Token) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    validated_token = auth_service.validate_jwt_token(token)

    if validated_token == None:
        raise credentials_exception
    return token


@router.post("/login")
async def login_user(detail: UserLogin, session: SessionDep):
    return auth_service.login_user(detail, session)
