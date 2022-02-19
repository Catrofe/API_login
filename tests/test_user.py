import pytest
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, drop_database

from app.database import User, build_engine, build_session_maker, setup_db
from app.models import UserRegister
from app.user import AddSuccess, add


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
        n_users = session.query(User).count()
        assert n_users == 0

    response = add(user, session_maker)
    assert isinstance(response, AddSuccess)
    assert isinstance(response.id, int)
    assert response.email == user.email

    with session_maker() as session:
        n_users = session.query(User).count()
        assert n_users == 1
