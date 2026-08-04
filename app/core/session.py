from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint
from fastapi import Depends, FastAPI
from app.core.config import settings

mysql_url = f"mysql+mysqlconnector://{settings.db_user}\
        :{settings.db_password}@{settings.db_host}:\
        {settings.db_port}/{settings.db_name}"

engine = create_engine(mysql_url)

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]
