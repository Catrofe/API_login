from fastapi import FastAPI
from models import UserLogin, UserRegister

app = FastAPI()


@app.post("/login")
def register_user(user: UserRegister):
    raise NotImplementedError


@app.post("/login")
def login(user: UserLogin):
    raise NotImplementedError


@app.put("/login")
def logout():
    raise NotImplementedError


@app.get("/login")
def search_users_logged():
    raise NotImplementedError
