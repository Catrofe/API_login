from fastapi import FastAPI
from models import UserLogin, UserRegister
from user import UserManager

app = FastAPI(debug=True)
db_user = UserManager()


@app.post("/login", status_code=201)
def register_user(user: UserRegister):
    create = db_user.creating_object(dict(user))
    print(create)
    if create:
        return "New user registered"


@app.put("/login")
def login(user: UserLogin):
    raise NotImplementedError


@app.put("/login{codigo}")
def validation(codigo):
    raise NotImplementedError


@app.put("/logout")
def logout():
    raise NotImplementedError


@app.get("/login")
def search_users_logged():
    raise NotImplementedError
