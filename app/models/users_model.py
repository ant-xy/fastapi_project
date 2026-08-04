from typing import Annotated
from sqlmodel import Field, SQLModel, UniqueConstraint

class UsersBase(SQLModel):
    __table_args__ = (
        UniqueConstraint("username"),
    )
    username: str

class Users(UsersBase, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    password: str

class UsersCreate(UsersBase):
    password: str

class UsersRead(UsersBase):
    id: int
