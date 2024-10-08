from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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


if __name__ == "__main__":
    uvicorn.run(app)
