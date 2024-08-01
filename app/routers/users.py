from typing import Annotated
from fastapi import APIRouter, Depends
from ..internal import db, models
from ..dependencies import security

router = APIRouter(prefix="/api/users", tags=["users"], dependencies=[], responses={})


@router.get("/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return current_user


@router.post("/create")
async def create_user(
    current_user: Annotated[models.User, Depends(security.get_current_admin_user)],
    new_user: models.NewUser,
):
    db.create_user(new_user)
    return new_user
