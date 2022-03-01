from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database

from app.main import app, register_user, startup_event
from app.user import UserRegister

client = TestClient(app)


url = "sqlite:///db.sqlite3"


def test_register_valid_user():
    startup_event()

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 201
    assert response.json() == {"email": "test@test.com", "id": 1}

    drop_database(url)


def test_register_email_duplicate():
    user = UserRegister(email="test@test.com", name="test_user", password="Ma123456")
    startup_event()

    register_user(user)

    response = client.post(
        "/register",
        json={"email": "test@test.com", "name": "test_user", "password": "Ma123456"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "EMAIL_ALREADY_EXISTS"}

    drop_database(url)


def test_login_data_correctly():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.patch(
        "/login", json={"email": "ch@test.com", "password": "Ma123456"}
    )

    assert response.status_code == 200
    assert response.json() == {"email": "ch@test.com", "status": "LOGIN_SUCCESSFUL"}

    drop_database(url)


def test_login_should_bad_request():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.patch(
        "/login", json={"email": "ch@test.com", "password": "Ma12345"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "EMAIL_OR_PASSWORD_INVALID"}

    drop_database(url)


def test_logout_successful():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    login = client.patch(
        "/login", json={"email": "ch@test.com", "password": "Ma123456"}
    )

    assert login.status_code == 200

    response = client.patch("/logout/1")

    assert response.status_code == 200
    assert response.json() == {"email": "ch@test.com", "status": "LOGOUT_SUCCESSFUL"}

    drop_database(url)


def test_logout_return_status_500():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    login = client.patch(
        "/login", json={"email": "ch@test.com", "password": "Ma123456"}
    )

    assert login.status_code == 200

    response = client.patch("/logout/2")

    assert response.status_code == 500
    assert response.json() == {"detail": "USER_NOT_FOUND"}

    drop_database(url)


def test_logout_bad_request():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.patch("/logout/1")

    assert response.status_code == 400
    assert response.json() == {"detail": "USER_NOT_LOGGED"}

    drop_database(url)


def test_verify_if_user_logged():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    login = client.patch(
        "/login", json={"email": "ch@test.com", "password": "Ma123456"}
    )

    assert login.status_code == 200

    response = client.get("/logged/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": "ch@test.com", "status": "USER_LOGGED"}

    drop_database(url)


def test_verify_if_user_not_logged():
    startup_event()

    user = UserRegister(email="ch@test.com", name="test_user", password="Ma123456")

    register_user(user)

    response = client.get("/logged/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "ch@test.com",
        "status": "USER_NOT_LOGGED",
    }

    drop_database(url)


def test_expected_return_status_400():
    startup_event()

    response = client.get("/logged/2")

    assert response.status_code == 400
    assert response.json() == {"detail": "USER_NOT_FOUND"}

    drop_database(url)
