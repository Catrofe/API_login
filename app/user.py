import re
from typing import Tuple

import bcrypt
from sqlalchemy.orm import sessionmaker

from app.database import User
from app.models import UserRegister


def add(user: UserRegister, session_maker: sessionmaker) -> Tuple[int, str, int]:
    if verify_email_already_exists(user.email, session_maker):
        return 0, "Email already exists", 409

    password_verify = validate_password(user.password)
    if not password_verify:
        return 0, "Password Invalid", 400

    password = encrypt_password(user.password)
    try:
        user_add = User(name=user.name, email=user.email, password=password)
        with session_maker() as session:
            session.add(user_add)
            session.commit()
            return user_add.id, "Success", 201
    except Exception:
        return 0, "Error", 500


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
