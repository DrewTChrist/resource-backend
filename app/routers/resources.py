from fastapi import APIRouter, Depends, HTTPException

from app.internal.db import resources
from app.internal import models
from app.dependencies import security

router = APIRouter(
    prefix="/api/resources",
    tags=["resources"],
    dependencies=[Depends(security.get_current_active_user)],
    responses={},
)


def iter_file(file_name: str):
    with open(file_name, "rb") as file:
        yield from file


@router.get("/")
async def read_resources() -> list[models.Resource]:
    resource_list = resources.get_resources()
    return resource_list


@router.get("/{resource_id}")
def read_resource(resource_id: int) -> models.Resource:
    resource = resources.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
