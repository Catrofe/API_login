from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def build_engine(db_url: str) -> Engine:
    return create_engine(db_url)


def build_session_maker(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine)


def setup_db(engine: Engine) -> None:
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    logged = Column(Boolean, nullable=False, default=False)
