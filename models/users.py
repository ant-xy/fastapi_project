from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint
from pydantic import BaseModel


class UsersBase(SQLModel):
    __table_args__ = (
        UniqueConstraint("username"),
    )
    username: str

class Users(UsersBase, table=True):
    id: Annotated[int, Field(default=None, primary_key=True)]
    password: str

class UsersCreate(UsersBase):
    password: str

class UsersRead(UsersBase):
    id: int

class Payload(BaseModel):
    status: int
    message: str
    data: list[UsersRead] | UsersRead

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    jwt: str
    token_type: str
