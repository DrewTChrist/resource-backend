# Decent blog post with celery example to handle background process
# https://testdriven.io/blog/fastapi-and-celery/
import os
import pathlib
from dataclasses import dataclass
from celery import Celery
from app.internal import configuration


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


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


@celery.task(name="index_files")
def index_files():
    # directory = configuration.get_config().resource_directory
    # file_list = get_file_list(directory)
    return True
