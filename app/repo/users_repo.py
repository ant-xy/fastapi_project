from app.core.session import SessionDep
from app.models.users_model import UsersCreate, Users

import sqlalchemy
from sqlmodel import select

def add_user_to_db(user: UsersCreate, session: SessionDep):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except sqlalchemy.exc.IntegrityError as ex:
        return "Something went wrong, try again later"
    return user


def get_all_users(session: SessionDep):
    return session.exec(select(Users)).all()
