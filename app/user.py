import re
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

    if not validate_password(user.password):
        return AddError(reason="BAD_REQUEST", message="Invalid password")

    password = encrypt_password(user.password)
    try:
        user_add = User(name=user.name, email=user.email, password=password)
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
    crypt_password = bcrypt.hashpw(
        raw_password.encode("utf8"), bcrypt.gensalt(8)
    ).decode()
    return crypt_password


def validate_password(password: str) -> bool:
    if (
        bool(re.search(r"[a-z]", password))
        and bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[1-9]", password))
    ):
        return True
    return False
