# Decent blog post with celery example to handle background process
# https://testdriven.io/blog/fastapi-and-celery/
import os
import pathlib
from dataclasses import dataclass


@dataclass
class ResourceFile:
    file_name: str
    full_path: str
    size: int


def get_file_list(directory: str) -> list[ResourceFile]:
    path = pathlib.Path(directory)
    resources = []
    for file in path.iterdir():
        # should find way to calculate
        # length of mp4
        resource = ResourceFile(
            file_name=file.name,
            full_path=str(file.absolute()),
            size=file.lstat().st_size,
        )
        resources.append(resource)
    return resources


def index_files(file_list: list[ResourceFile]):
    # insert into db
    pass
