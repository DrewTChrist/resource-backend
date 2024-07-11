from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources import RESOURCES

origins = [
    "https://sturdy-xylophone-4jvrqw47qv7fjxgw-5173.app.github.dev",
    "https://codespaces-blank-omega.vercel.app"
]

app = FastAPI()

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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
