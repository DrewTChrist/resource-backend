from typing import Annotated
from fastapi import APIRouter, Depends

from app.internal.db import users
from app.internal import models
from app.dependencies import security

router = APIRouter(prefix="/api/users", tags=["users"], dependencies=[], responses={})


@router.get("/", dependencies=[Depends(security.get_current_admin_user)])
async def get_users() -> list[models.User]:
    user_list = users.get_users()
    return user_list


@router.get("/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_user)]
):
    return current_user


@router.post(
    "/create", dependencies=[Depends(security.get_current_admin_user)], status_code=201
)
async def create_user(new_user: models.NewUser):
    users.create_user(new_user)
    return new_user


@router.post("/remove")
async def create_user(
    current_user: Annotated[models.User, Depends(security.get_current_admin_user)],
    user: models.User
):
    if current_user.username == user.username:
        raise HTTPException(status_code=403, detail="User cannot delete themselves")
    users.remove_user(user)
