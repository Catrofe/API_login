import re

import bcrypt
from database import User
from models import UserRegister


class UserManager:
    def creating_object(self, user: UserRegister) -> None:
        self.email = user["email"]
        self.password = user["password"]
        self.name = user["name"]

        create = self.manager()
        return create

    def validate_email(self) -> bool:
        return bool(
            re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", self.email)
        )

    def validate_name(self) -> bool:
        if len(self.name) >= 3 and len(self.name) <= 255:
            return True

        return False

    def validate_password(self) -> bool:
        if len(self.password) >= 8 and len(self.password) <= 255:
            if (
                bool(re.search(r"[a-z]", self.password)) and 
                bool(re.search(r"[A-Z]", self.password)) and 
                bool(re.search(r"[1-9]", self.password))
            ):
                return True

        return False

    def encrypt_password(self, password) -> str:
        password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(8)).decode()
        return password

    def manager(self) -> bool:
        email_verify = self.validate_email()
        password_verify = self.validate_password()
        name_verify = self.validate_name()
        password = self.encrypt_password(self.password)

        if email_verify and password_verify and name_verify:
            User.create(email=self.email, name=self.name, password=password)
            return True
        else:
            return False
