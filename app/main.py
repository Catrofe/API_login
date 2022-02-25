from dataclasses import dataclass

from fastapi import FastAPI, HTTPException
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.database import build_engine, build_session_maker, setup_db
from app.models import (
    GetLoggedOutput,
    LoggedOutput,
    UserLogin,
    UserOutput,
    UserRegister,
)
from app.user import (
    AddSuccess,
    AlterStatusLogin,
    Error,
    Logged,
    add,
    return_user_logged,
    update_login,
    update_logout,
)

app = FastAPI(debug=True)


@dataclass
class ServerContext:
    engine: Engine
    session_maker: sessionmaker


# "postgresql+psycopg2://postgres:root@localhost:5432/login_api"
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


@app.patch("/login", response_model=LoggedOutput)
def login_user(user: UserLogin) -> LoggedOutput:
    response = update_login(user, context.session_maker)

    if isinstance(response, AlterStatusLogin):
        return LoggedOutput(email=response.email, status=response.status)

    if response.reason == "BAD_REQUEST":
        raise HTTPException(400, response.message)

    raise HTTPException(500, response.message)


@app.patch("/logout/{id}", response_model=LoggedOutput)
def logout_user(id: int) -> LoggedOutput:
    response = update_logout(id, context.session_maker)

    if isinstance(response, AlterStatusLogin):
        return LoggedOutput(email=response.email, status=response.status)

    if response.reason == "BAD_REQUEST":
        raise HTTPException(400, response.message)

    raise HTTPException(500, response.message)


@app.get("/logged/{id_user}", response_model=GetLoggedOutput)
def is_user_logged(id_user: int) -> GetLoggedOutput:
    response = return_user_logged(id_user, context.session_maker)

    if isinstance(response, Logged):
        return GetLoggedOutput(
            id=response.id, email=response.email, status=response.status
        )

    if isinstance(response, Error):
        raise HTTPException(400, response.message)

    raise HTTPException(500, response.message)
