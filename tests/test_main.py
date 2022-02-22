from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database

from app.main import app, register_user, startup_event
from app.user import UserRegister


def drop_db():
    url = "sqlite:///db.sqlite3"
    if database_exists(url):
        drop_database(url)


def test_register_valid_user():
    startup_event()
    client = TestClient(app)
    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 201
    assert response.json() == {"email": "test@test.com", "id": 1}

    drop_db()


def test_register_email_duplicate():
    client = TestClient(app)
    startup_event()

    response = client.post("/register")

    user = UserRegister(email="test@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}

    drop_db()
