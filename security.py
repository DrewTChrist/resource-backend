import typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
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
    return user
