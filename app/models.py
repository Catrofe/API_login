from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    nome: str
    senha: str


class UserLogin(UserRegister):
    nome: str
    senha: str
