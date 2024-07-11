from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from db import get_user
from models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def _fake_decode_token(token):
    return User(
        username=token + "fakedecode",
        email="johndoe@example.com",
        full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = _fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_402_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
