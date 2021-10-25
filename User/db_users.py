import databases
import sqlalchemy
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from User.schemas import UserDB

DATABASE_URL = "sqlite:///sqlite2.db"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class UserModel(OrmarBaseUserModel):
    class Meta:
        tablename = "users_2"
        metadata = metadata
        database = database


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


def get_user_db():
    yield OrmarUserDatabase(UserDB, UserModel)