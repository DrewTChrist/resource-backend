from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str

