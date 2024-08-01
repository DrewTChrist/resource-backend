from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.internal import models
from app.dependencies import security

router = APIRouter(prefix="/api/auth", tags=["auth"], dependencies=[], responses={})


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> models.Token:
    user = security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")
