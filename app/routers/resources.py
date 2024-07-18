from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from ..dependencies import db, models, security
from ..dependencies.resources import RESOURCES

router = APIRouter(
    prefix="/api/resources", tags=["resources"], dependencies=[], responses={}
)


def iter_file(file_name: str):
    with open(file_name, "rb") as file:
        yield from file


@router.get("/")
async def read_resources(
    current_user: Annotated[models.User, Depends(security.get_current_active_user)]
):
    return RESOURCES


@router.get("/{resource_id}")
def read_resource(
    resource_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_active_user)],
):
    # here find resource in db and get path on disk
    file_name = ""
    return StreamingResponse(iter_file(file_name), media_type="video/mp4")
