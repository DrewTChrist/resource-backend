from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    username: str
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class NewUser(User):
    password: str


class Resource(BaseModel):
    resource_id: Union[int, None] = None
    name: str
    path: str
    size: int
