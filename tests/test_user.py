import pytest
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, drop_database

from app.database import User, build_engine, build_session_maker, setup_db
from app.models import UserRegister
from app.user import add


@pytest.fixture
def engine() -> Engine:
    url = "sqlite:///db.sqlite3"
    if database_exists(url):
        drop_database(url)
    eng = build_engine(url)
    setup_db(eng)

    yield eng

    drop_database(url)


def test_add_happy_path(engine: Engine):
    user = UserRegister(email="test@test.com", name="test_user", password="Ma123456")
    session_maker = build_session_maker(engine)

    with session_maker() as session:
        users = session.query(User).count()
        print(users)

    response = add(user, session_maker)

    assert response[0] > 0
    assert response[1] == "Success"
    assert response[2] == 201
