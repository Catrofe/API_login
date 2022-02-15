from peewee import BitField, CharField, Model
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(
    "postgres", user="postgres", password="root", port="5432", host="localhost"
)


class User(Model):
    email = CharField(null=False, unique=True)
    name = CharField(null=False, max_length=255)
    password = CharField(null=False, max_length=65)
    Logged = BitField(null=False, default=0)

    class Meta:
        database = db


db.create_tables([User])
