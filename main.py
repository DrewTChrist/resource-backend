from typing import Union, Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import models
from resources import RESOURCES
from security import get_current_user

origins = [
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev",
    "https://codespaces-blank-omega.vercel.app"
]

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/resources")
def read_resources():
    return RESOURCES


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/users/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
