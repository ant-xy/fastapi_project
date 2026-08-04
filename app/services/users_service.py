from app.models.users_model import UsersCreate, Users
from app.core.session import SessionDep

from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.bcrypt import BcryptHasher

import app.repo.users_repo as repo_funcs
from app.schemas.response.users_response import UsersResponseData

password_hash = PasswordHash((BcryptHasher(),))

def hash_password_user(user: UsersCreate):
    user.password = password_hash.hash(user.password)
    return user

def return_all_users_or_one(user_id: int, session: SessionDep):
    user = session.get(Users, user_id)

    if not user:
        all_users = repo_funcs.get_all_users(session)
        user_response_data = UsersResponseData(status=200, message="success", data=all_users)
        return user_response_data

    user_response_data = UsersResponseData(status=200, message="success", data=user)
    return user_response_data


