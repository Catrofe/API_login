from pydantic import BaseModel, Field

_email_field = Field(regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_name_field = Field(min_length=3, max_length=255)
_password_field = Field(min_length=8, max_length=255)


class UserRegister(BaseModel):
    email: str = _email_field
    name: str = _name_field
    password: str = _password_field


class UserLogin(BaseModel):
    email: str = _email_field
    password: str = _password_field


class UserOutput(BaseModel):
    id: int
    email: str = _email_field
