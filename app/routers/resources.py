from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.dependencies import security
from app.internal.resources import RESOURCES

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
async def read_resources():
    return RESOURCES


@router.get("/{resource_id}")
def read_resource(resource_id: int):
    # here find resource in db and get path on disk
    _ = resource_id
    file_name = ""
    return StreamingResponse(iter_file(file_name), media_type="video/mp4")
