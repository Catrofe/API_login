from fastapi import FastAPI
from models import User

app = FastAPI()


@app.post("/register")
def register_user(user: User):
    return "In Construction"
