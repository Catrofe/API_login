import re

from pydantic import BaseModel, Field, validator

_email_field = Field(regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_name_field = Field(min_length=3, max_length=255)


class UserRegister(BaseModel):
    email: str = _email_field
    name: str = _name_field
    password: str = Field(min_length=8, max_length=255)

    @validator("password")
    def password_must_contain_upper_letter(cls, password: str) -> str:
        if not bool(re.search(r"[A-Z]", password)):
            raise ValueError("Password must contain an upper letter")
        return password

    @validator("password")
    def password_must_contain_lower_letter(cls, password: str) -> str:
        if not bool(re.search(r"[a-z]", password)):
            raise ValueError("Password must contain a lower letter")
        return password

    @validator("password")
    def password_must_contain_number(cls, password: str) -> str:
        if not bool(re.search(r"[0-9]", password)):
            raise ValueError("Password must contain a number")
        return password


class UserLogin(BaseModel):
    email: str = _email_field
    password: str


class UserOutput(BaseModel):
    id: int
    email: str = _email_field
