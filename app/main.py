from fastapi import FastAPI
from models import UserRegister
from user import UserRepository

app = FastAPI(debug=True)
db_user = UserRepository()


@app.post("/register", status_code=201)
def register_user(user: UserRegister):
    create = db_user.creating_object(user.dict())
    if create:
        return f"New user registered, ID: {create}"
    if not create:
        return "Error, new user not registered"
