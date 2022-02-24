import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, drop_database

from app.database import build_engine, build_session_maker, setup_db
from app.main import app, register_user
from app.user import UserRegister

client = TestClient(app)


@pytest.fixture
def engine() -> Engine:
    url = "sqlite:///db.sqlite3"
    if database_exists(url):
        drop_database(url)
    eng = build_engine(url)
    setup_db(eng)

    yield eng

    drop_database(url)


def test_register_valid_user(engine: Engine):
    build_session_maker(engine)

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 201
    assert response.json() == {"email": "test@test.com", "id": 1}


def test_register_email_duplicate(engine: Engine):
    user = UserRegister(email="test@test.com", name="test_user", password="Ma123456")
    build_session_maker(engine)

    register_user(user)

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}


# def test_login_data_correctly(engine: Engine):
#     session_maker = build_session_maker(engine)

#     user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

#     register_user(user)

#     response = client.patch(
#         "/login",
#         json={"email": "ch@test.com", "password": "Ma123456"}
#     )

#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "email": "ch@test.com"}

# def test_login_should_bad_request(engine: Engine):
#     session_maker = build_session_maker(engine)

#     user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

#     register_user(user)

#     response = client.patch(
#         "/login",
#         json={"email": "ch@test.com", "password": "Ma12345"}
#     )

#     assert response.status_code == 400
#     assert response.json() == {"detail": "Email or password invalid"}
