from dataclasses import dataclass

from fastapi import FastAPI, HTTPException
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.database import build_engine, build_session_maker, setup_db
from app.models import UserOutput, UserRegister
from app.user import AddSuccess, add

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


@app.post("/register", status_code=201, response_model=UserOutput)
def register_user(user: UserRegister) -> UserOutput:
    response = add(user, context.session_maker)

    if isinstance(response, AddSuccess):
        return UserOutput(id=response.id, email=response.email)

    if response.reason == "CONFLICT":
        raise HTTPException(409, response.message)

    raise HTTPException(500, response.message)
