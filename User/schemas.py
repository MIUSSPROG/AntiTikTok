from fastapi_users import models


class User(models.BaseUser):
    username: str


class UserCreate(models.BaseUserCreate):
    username: str


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass
