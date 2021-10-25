from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from User.db_users import database
from User.schemas import UserDB
from User.users import fastapi_users, jwt_authentication, current_active_user

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_users_router(), prefix="/users", tags=["users"]
)


@user_router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@user_router.on_event("startup")
async def startup():
    await database.connect()


@user_router.on_event("shutdown")
async def shutdown():
    await database.disconnect()
