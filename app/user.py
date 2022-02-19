from dataclasses import dataclass
from typing import Literal

import bcrypt
from sqlalchemy.orm import sessionmaker

from app.database import User
from app.models import UserRegister


@dataclass
class AddSuccess:
    id: int
    email: str


@dataclass
class AddError:
    reason: Literal["BAD_REQUEST", "CONFLICT", "UNKNOWN"]
    message: str


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


def verify_email_already_exists(email_user: str, session_maker: sessionmaker) -> bool:
    with session_maker() as session:
        return bool(session.query(User.email).filter_by(email=email_user).count())


def encrypt_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()
