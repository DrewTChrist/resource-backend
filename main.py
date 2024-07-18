from datetime import timedelta
from typing import Union, Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.dependencies import models, security
from app.routers import users, resources, auth

origins = [
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev",
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev/*",
    "https://codespaces-blank-omega.vercel.app",
    "https://codespaces-blank-omega.vercel.app/*",
]

app = FastAPI()

app.include_router(users.router)
app.include_router(resources.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/advanced/custom-response/
# app.mount("/static", StaticFiles(directory="assets"), name="static")


if __name__ == "__main__":
    load_dotenv()
    import uvicorn

    uvicorn.run(app)
