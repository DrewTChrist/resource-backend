import os
from typing import BinaryIO

import celery
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from app.background import tasks
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


@router.post("/reindex")
def reindex():
    try:
        task = tasks.index_files.delay()
    except celery.exceptions.OperationalError as e:
        raise HTTPException(status_code=500, detail="Message queue unavailable") from e
    return {"task_id": task.id}


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


def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 10_000
):
    """Send a file in chunks using Range Requests specification RFC7233

    `start` and `end` parameters are inclusive due to specification
    """
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def _get_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    def _invalid_range():
        return HTTPException(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid request range (Range:{range_header!r})",
        )

    try:
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise _invalid_range()

    if start > end or start < 0 or end > file_size - 1:
        raise _invalid_range()
    return start, end


def range_requests_response(request: Request, file_path: str, content_type: str):
    """Returns StreamingResponse using Range Requests of a given file"""

    file_size = os.stat(file_path).st_size
    range_header = request.headers.get("range")

    headers = {
        "content-type": content_type,
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "access-control-expose-headers": (
            "content-type, accept-ranges, content-length, "
            "content-range, content-encoding"
        ),
    }
    start = 0
    end = file_size - 1
    status_code = status.HTTP_200_OK

    if range_header is not None:
        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["content-length"] = str(size)
        headers["content-range"] = f"bytes {start}-{end}/{file_size}"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    return StreamingResponse(
        send_bytes_range_requests(open(file_path, mode="rb"), start, end),
        headers=headers,
        status_code=status_code,
    )


# https://github.com/fastapi/fastapi/discussions/7718
# https://stackoverflow.com/questions/68031189/fetching-videomp4-format-using-axios-in-react-and-displaying-in-html-video
@router.get("/stream/{resource_id}")
def stream_resource(resource_id: int, request: Request):
    resource = resources.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return range_requests_response(
        request, file_path=resource.path, content_type="video/mp4"
    )
    # return StreamingResponse(
    #     iter_file(resource.path),
    #     status_code=206,
    #     media_type="video/mp4",
    #     headers={
    #         # "Accept-Ranges": "bytes",
    #         "Content-Length": str(2299653),
    #         # "Content-Range": F"bytes {asked}-{sz-1}/{sz}",
    #     },
    # )
