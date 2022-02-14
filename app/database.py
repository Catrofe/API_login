from peewee import CharField, Model
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(
    "postgres", user="postgres", password="root", port="5432", host="localhost"
)


class User(Model):
    email = CharField(null=False, unique=True)
    name = CharField(null=False, min_length=3, max_length=255)
    password = CharField(null=False, min_length=8, max_length=255)

    class Meta:
        database = db


db.create_tables([User])
