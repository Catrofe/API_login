from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from models import UserRegister
from user import UserRepository

app = FastAPI(debug=True)
db_user = UserRepository()


@app.post("/register", status_code=201)
def register_user(user: UserRegister) -> Optional[Dict[str, str]]:
    id, comment, status_code = db_user.add(user.dict())

    if id:
        return {"New user registered, ID:": str(id)}
    else:
        raise HTTPException(status_code, comment)
