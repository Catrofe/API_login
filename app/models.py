from pydantic import BaseModel


class User(BaseModel):
    email: str
    nome: str
    senha: str
