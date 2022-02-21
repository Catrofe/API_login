import logging

from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database

from app.main import app, register_user, startup_event
from app.user import UserRegister


def drop():
    url = "sqlite:///db.sqlite3"
    if database_exists(url):
        drop_database(url)
    else:
        drop_database(url)


def test_register_user_should_add_success():
    startup_event()
    client = TestClient(app)
    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 201
    assert response.json() == {"email": "test@test.com", "id": 1}

    drop()


def test_register_user_should_code_409():
    client = TestClient(app)
    startup_event()

    response = client.post("/register")

    user = UserRegister(email="test@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    logging.critical(response)

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}

    drop()
