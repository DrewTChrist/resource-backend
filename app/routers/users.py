"""Users related routes

This module holds the routes for managing users of the application and other
tightly coupled data (e.g. favorites).
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.internal.db import users
from app.internal import models
from app.dependencies import security

router = APIRouter(prefix="/api/users", tags=["users"], dependencies=[], responses={})


@router.get("/", dependencies=[Depends(security.get_current_admin_user)])
async def get_users() -> list[models.User]:
    """Returns a list of all users

    This endpoint is only accessible to administrators.
    """
    user_list = users.get_users()
    return user_list


@router.get("/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_user)]
):
    """Retrieve the current user from the database

    The current user would be the user matching the auth token in the request
    to this endpoint. This endpoint is accessible to any user.
    """
    return current_user


@router.post(
    "/",
    dependencies=[Depends(security.get_current_admin_user)],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(new_user: models.NewUser):
    """Create a new user in the database

    This endpoint is only accessible to administrators.
    """
    users.create_user(new_user)
    return new_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    current_user: Annotated[models.User, Depends(security.get_current_admin_user)],
    user_id: int,
):
    """Remove a user from the database

    Returns an empty reponse and will throw an error if a user tries to remove
    themselves from the database. This endpoint is only accessible to
    administrators.
    """
    if current_user.user_id == user_id:
        raise HTTPException(status_code=403, detail="User cannot delete themselves")
    users.remove_user(user_id)
    return {}
