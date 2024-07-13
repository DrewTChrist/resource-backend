from typing import Union, Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import db
import models
from resources import RESOURCES
from security import get_current_user, get_current_active_user

origins = [
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev",
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev/*",
    "https://codespaces-blank-omega.vercel.app",
    "https://codespaces-blank-omega.vercel.app/*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="assets"), name="static")

def fake_hash_password(password: str):
    return "fakehashed" + password

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/resources")
async def read_resources(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return RESOURCES


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = db.fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = models.UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/api/users/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return current_user


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
