# Decent blog post with celery example to handle background process
# https://testdriven.io/blog/fastapi-and-celery/
import os
import pathlib
from celery import Celery
from app.internal import configuration
from app.internal import models
from app.internal.db import resources


celery_instance = Celery(__name__)
celery_instance.conf.broker_url = configuration.get_config().celery_broker_url
celery_instance.conf.result_backend = configuration.get_config().celery_result_backend


def get_file_list(directory: str) -> list[models.Resource]:
    path = pathlib.Path(directory)
    resources = []
    for file in path.iterdir():
        if file.is_dir():
            [resources.append(f) for f in get_file_list(file)]
        else:
            resource = models.Resource(
                name=file.name,
                path=str(file.absolute()),
                size=file.lstat().st_size,
            )
            resources.append(resource)
    return resources


@celery_instance.task(name="index_files")
def index_files():
    directory = configuration.get_config().resource_directory
    file_list = get_file_list(directory)
    for file in file_list:
        resources.create_resource(file)
