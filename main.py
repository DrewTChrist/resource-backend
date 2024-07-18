from datetime import datetime, timedelta, timezone
from typing import Union, Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import db
import models
from resources import RESOURCES
import security

origins = [
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev",
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev/*",
    "https://codespaces-blank-omega.vercel.app",
    "https://codespaces-blank-omega.vercel.app/*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/advanced/custom-response/
app.mount("/static", StaticFiles(directory="assets"), name="static")


@app.get("/api/resources")
async def read_resources(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return RESOURCES


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> models.Token:
    user = security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    return models.Token(access_token=access_token, token_type="bearer")

def iter_file(file_name: str):
    with open(file_name, "rb") as file:
        yield from file

@app.get("/api/resource/{content_id}")
def read_resource(
    resource_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_active_user)],
):
    # here find resource in db and get path on disk
    file_name = ""
    return StreamingResponse(iter_file(file_name), media_type="video/mp4")


@app.get("/api/users/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return current_user


@app.post("/api/users/create/")
async def create_user(
    current_user: Annotated[models.User, Depends(security.get_current_admin_user)],
    new_user: models.NewUser
):
    db.create_user(new_user)
    return new_user


if __name__ == "__main__":
    load_dotenv()
    import uvicorn

    uvicorn.run(app)
