from dataclasses import dataclass
from typing import Literal

import bcrypt
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from app.database import User
from app.models import UserLogin, UserRegister


@dataclass
class AddSuccess:
    id: int
    email: str


@dataclass
class AddError:
    reason: Literal["BAD_REQUEST", "CONFLICT", "UNKNOWN"]
    message: str


@dataclass
class Logged:
    id: int
    email: str
    status: Literal["User logged", "User not logged"]


def add(user: UserRegister, session_maker: sessionmaker) -> AddSuccess | AddError:
    if verify_email_already_exists(user.email, session_maker):
        return AddError(reason="CONFLICT", message="Email already exists")

    try:
        user_add = User(
            name=user.name, email=user.email, password=encrypt_password(user.password)
        )
        with session_maker() as session:
            session.add(user_add)
            session.commit()

            return AddSuccess(id=user_add.id, email=user_add.email)

    except Exception as exc:
        return AddError(reason="UNKNOWN", message=repr(exc))


def update_login(user: UserLogin, session_maker: sessionmaker) -> AddSuccess | AddError:
    try:
        with session_maker() as session:
            user_db = session.query(User.id, User.email, User.password).filter_by(
                email=user.email
            )
            password_db = user_db[0][2]

        if user_db[0][1] == user.email:
            user.password = user.password.encode("utf8")
            password_db = password_db.encode("utf8")

        if bcrypt.checkpw(user.password, password_db):
            with session_maker() as session:
                stmt = update(User).values(logged=1).where(User.id == user_db[0][0])

                session.execute(stmt)
                session.commit()

            return AddSuccess(id=user_db[0][0], email=user_db[0][1])

        return AddError(reason="BAD_REQUEST", message="Email or password invalid")

    except IndexError:
        return AddError(reason="UNKNOWN", message="User not found")


def update_logout(id: int, session_maker: sessionmaker) -> AddSuccess | AddError:
    try:
        with session_maker() as session:
            user_db = session.query(
                User.id, User.email, User.password, User.logged
            ).filter_by(id=id)

        if not user_db[0][3]:
            return AddError(reason="BAD_REQUEST", message="User not logged")

        if not user_db.count():
            return AddError(reason="UNKNOWN", message="User not exists")

        if user_db[0][3] == id:
            with session_maker() as session:
                stmt = update(User).values(logged=0).where(User.id == id)

                session.execute(stmt)
                session.commit()

            return AddSuccess(id=id, email=user_db[0][1])
    
    except IndexError:
        return AddError(reason="UNKNOWN", message="User not found")


def return_user_logged(id: int, session_maker: sessionmaker) -> Logged | AddError:
    try:
        with session_maker() as session:
            user_db = session.query(User.id, User.email, User.logged).filter_by(id=id)

        if user_db[0][2]:
            return Logged(id=user_db[0][0], email=user_db[0][1], status="User logged")

        if not user_db[0][2]:
            return Logged(
                id=user_db[0][0], email=user_db[0][1], status="User not logged"
            )

    except TypeError:
        return AddError(reason="UNKNOWN", message="User not found")

    except IndexError:
        return AddError(reason="UNKNOWN", message="User not found")


def verify_email_already_exists(email_user: str, session_maker: sessionmaker) -> bool:
    with session_maker() as session:
        return bool(session.query(User.email).filter_by(email=email_user).count())


def encrypt_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()
