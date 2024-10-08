from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from app.internal import configuration
from app.internal.db import users
from app.internal import models
from app.internal import hashing

SECRET_KEY = configuration.get_config().jwt_signature
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def authenticate_user(username: str, password: str) -> Union[models.UserInDB, None]:
    user = users.get_user(username)
    if not user:
        return None
    if not hashing.verify_password(password, user.hashed_password):
        return None
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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> models.User:
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
        token_data = models.TokenData(username=username)
    except InvalidTokenError as token_err:
        raise credentials_exception from token_err
    user = users.get_user(token_data.username)
    if not user:
        raise credentials_exception

    return models.User(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        disabled=user.disabled,
        admin=user.admin,
    )


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
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
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Internal Server Error",
#         )


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
