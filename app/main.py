from dataclasses import dataclass
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.database import build_engine, build_session_maker, setup_db
from app.models import UserRegister
from app.user import add

app = FastAPI(debug=True)


@dataclass
class ServerContext:
    engine: Engine
    session_maker: sessionmaker


engine = build_engine("sqlite:///db.sqlite3")
context = ServerContext(engine=engine, session_maker=build_session_maker(engine))


@app.on_event("startup")
def startup_event() -> None:
    setup_db(context.engine)


@app.post("/register", status_code=201, response_model=UserRegister)
def register_user(user: UserRegister) -> Optional[Dict[str, str]]:
    id, comment, status_code = add(user, context.session_maker)

    if id:
        return {"New user registered, ID:": str(id)}
    else:
        raise HTTPException(status_code, comment)
