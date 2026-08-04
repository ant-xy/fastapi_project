from pydantic import BaseModel
from app.models.users_model import UsersRead

class UsersResponseData(BaseModel):
    status: int
    message: str
    data: list[UsersRead] | UsersRead

class Token(BaseModel):
    jwt: str
    token_type: str
