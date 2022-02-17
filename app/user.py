import re
from typing import Dict, Tuple

import bcrypt
from database import User, create_tables, session
from sqlalchemy.exc import ProgrammingError


class UserRepository:
    def add(self, user: Dict[str, str]) -> Tuple[int, str, int]:
        self.email = user["email"]
        self.password = user["password"]
        self.name = user["name"]

        try:
            session.query(User).all()
        except ProgrammingError:
            create_tables()

        if self.verify_email_already_exists(self.email):
            return 0, "Email already exists", 409

        email_verify = validate_email(self.email)
        if not email_verify:
            return 0, "Email Invalid", 400

        password_verify = self.validate_password()
        if not password_verify:
            return 0, "Password Invalid", 400

        name_verify = self.validate_name()
        if not name_verify:
            return 0, "Name Invalid", 400

        password = self.encrypt_password(self.password)

        if email_verify and password_verify and name_verify:
            user_add = User(name=self.name, email=self.email, password=password)
            session.add(user_add)
            session.commit()
            return user_add.id, "Sucess", 201

        return 0, "Error", 500

    def verify_email_already_exists(self, email_user: str) -> bool:
        return bool(session.query(User.email).filter_by(email=email_user).count())

    def validate_name(self) -> bool:
        if len(self.name) >= 3 and len(self.name) <= 255:
            return True

        return False

    def validate_password(self) -> bool:
        if len(self.password) >= 8 and len(self.password) <= 255:
            if (
                bool(re.search(r"[a-z]", self.password))
                and bool(re.search(r"[A-Z]", self.password))
                and bool(re.search(r"[1-9]", self.password))
            ):
                return True
        return False

    def encrypt_password(self, raw_password: str) -> str:
        crypt_password = bcrypt.hashpw(
            raw_password.encode("utf8"), bcrypt.gensalt(8)
        ).decode()
        return crypt_password


def validate_email(email: str) -> bool:
    return bool(re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email))
