import databases
import ormar
import sqlalchemy

DATABASE_URL = "sqlite:///sqlite2.db"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)


class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database
