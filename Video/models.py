from typing import Optional, Union

import ormar
from db import metadata, database, MainMata
import datetime


class User(ormar.Model):
    class Meta(MainMata):
        pass

    id = ormar.Integer(primary_key=True)
    username = ormar.String(max_length=100)


class Video(ormar.Model):
    class Meta(MainMata):
        pass

    id = ormar.Integer(primary_key=True)
    title = ormar.String(max_length=50)
    description = ormar.String(max_length=500)
    file = ormar.String(max_length=1000)
    create_at = ormar.DateTime(default=datetime.datetime.now())
    user: Union[User, int, None] = ormar.ForeignKey(User)