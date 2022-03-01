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
class Error:
    reason: Literal["BAD_REQUEST", "CONFLICT", "UNKNOWN", "NOT_FOUND"]
    message: str


@dataclass
class Logged:
    id: int
    email: str
    status: Literal["USER_LOGGED", "USER_NOT_LOGGED"]


@dataclass
class AlterStatusLogin:
    email: str
    status: Literal["LOGIN_SUCCESSFUL", "LOGOUT_SUCCESSFUL"]


def add(user: UserRegister, session_maker: sessionmaker) -> AddSuccess | Error:
    if verify_email_already_exists(user.email, session_maker):
        return Error(reason="CONFLICT", message="EMAIL_ALREADY_EXISTS")

    try:
        user_add = User(
            name=user.name, email=user.email, password=encrypt_password(user.password)
        )
        with session_maker() as session:
            session.add(user_add)
            session.commit()

            return AddSuccess(id=user_add.id, email=user_add.email)

    except Exception as exc:
        return Error(reason="UNKNOWN", message=repr(exc))


def update_login(
    user: UserLogin, session_maker: sessionmaker
) -> AlterStatusLogin | Error:
    with session_maker() as session:
        user_db = (
            session.query(User.id, User.email, User.password)
            .filter(User.email == user.email)
            .one_or_none()
        )

    if user_db is None:
        return Error(reason="NOT_FOUND", message="USER_NOT_FOUND")

    if user_db.email == user.email:
        password_input_encrypt = user.password.encode("utf8")
        password_db = user_db.password.encode("utf8")

    if bcrypt.checkpw(password_input_encrypt, password_db):
        with session_maker() as session:
            stmt = update(User).where(User.id == user_db.id).values(logged=1)

            session.execute(stmt)
            session.commit()

        return AlterStatusLogin(email=user_db.email, status="LOGIN_SUCCESSFUL")

    return Error(reason="BAD_REQUEST", message="EMAIL_OR_PASSWORD_INVALID")


def update_logout(id: int, session_maker: sessionmaker) -> Error | AlterStatusLogin:
    with session_maker() as session:
        user_db = (
            session.query(User.id, User.email, User.logged)
            .filter(User.id == id)
            .one_or_none()
        )

    if user_db is None:
        return Error(reason="NOT_FOUND", message="USER_NOT_FOUND")

    if not user_db.logged:
        return Error(reason="BAD_REQUEST", message="USER_NOT_LOGGED")

    if user_db.id == id:
        with session_maker() as session:
            stmt = update(User).values(logged=0).where(User.id == id)

            session.execute(stmt)
            session.commit()

        return AlterStatusLogin(email=user_db.email, status="LOGOUT_SUCCESSFUL")

    return Error(reason="NOT_FOUND", message="USER_NOT_FOUND")


def return_user_logged(id: int, session_maker: sessionmaker) -> Logged | Error:
    with session_maker() as session:
        user_db = (
            session.query(User.id, User.email, User.logged)
            .filter(User.id == id)
            .one_or_none()
        )

    if user_db is None:
        return Error(reason="BAD_REQUEST", message="USER_NOT_FOUND")

    if user_db.logged:
        return Logged(id=user_db.id, email=user_db.email, status="USER_LOGGED")

    if not user_db.logged:
        return Logged(id=user_db.id, email=user_db.email, status="USER_NOT_LOGGED")

    return Error(reason="UNKNOWN", message="USER_NOT_FOUND")


def verify_email_already_exists(email_user: str, session_maker: sessionmaker) -> bool:
    with session_maker() as session:
        return bool(session.query(User.email).filter_by(email=email_user).count())


def encrypt_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()
