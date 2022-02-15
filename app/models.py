from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    name: str
    password: str
