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

video_file = "ForBiggerEscapes.mp4"


def fake_hash_password(password: str):
    return "fakehashed" + password


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/resources")
async def read_resources(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return RESOURCES


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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
    acess_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    return models.Token(acess_token=access_token, token_type="bearer")


@app.get("/api/resource/{content_id}")
def read_resource(
    resource_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_active_user)],
):
    def iter_file():
        with open(video_file, "rb") as file:
            yield from file

    return StreamingResponse(iter_file(), media_type="video/mp4")


@app.get("/api/users/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return current_user


if __name__ == "__main__":
    load_dotenv()
    import uvicorn

    uvicorn.run(app)
