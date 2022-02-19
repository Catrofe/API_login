from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    email: str = Field(regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    name: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserLogin(BaseModel):
    email: str = Field(regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    password: str = Field(min_length=8, max_length=255)


class UserOutput(BaseModel):
    id: int
    email: str
