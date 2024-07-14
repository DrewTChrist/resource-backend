from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

import bcrypt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from db import get_user
from models import User, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "46ae5877585e3b43e1e4ae5bc048396cc19fb7413ec5a71044eef7716a49f9c9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode("utf-8")
    hash_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hash_password_bytes)


def get_password_hash(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _fake_decode_token(token):
    return User(
        username=token + "fakedecode", email="johndoe@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# async def verify_user(request: Request):
#     try:
#         token = request.headers.get("Authorization")
#         if not token or not token.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         token = token.split("Bearer ")[1]
#         get_current_user(str(token))
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")

# https://github.com/tiangolo/fastapi/discussions/7900
# See here how to handle authentication of static files
# class AuthStaticFiles(StaticFiles):
#     def __init__(self, *args, **kwargs) -> None:

#         super().__init__(*args, **kwargs)

#     async def __call__(self, scope, receive, send) -> None:

#         assert scope["type"] == "http"

#         request = Request(scope, receive)
#         await verify_user(request)
#         await super().__call__(scope, receive, send)
