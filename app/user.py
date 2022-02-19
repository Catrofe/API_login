import re
from typing import Dict, Tuple

import bcrypt
from sqlalchemy.exc import ProgrammingError

from app.database import User, create_tables, session


def add(user: Dict[str, str]) -> Tuple[int, str, int]:
    try:
        session.query(User).all()
    except ProgrammingError:
        create_tables()

    if verify_email_already_exists(user["email"]):
        return 0, "Email already exists", 409

    password_verify = validate_password(user["password"])
    if not password_verify:
        return 0, "Password Invalid", 400

    if password_verify:
        password = encrypt_password(user["password"])
        user_add = User(name=user["name"], email=user["email"], password=password)
        session.add(user_add)
        session.commit()
        return user_add.id, "Sucess", 201

    return 0, "Error", 500


def verify_email_already_exists(email_user: str) -> bool:
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
