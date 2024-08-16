from typing import Union

from app.internal.db import get_connection_pool
from app.internal import models
from app.internal import hashing


def get_resources() -> list[models.Resource]:
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM resources;")
    resources = cursor.fetchall()
    resource_list = []
    cursor.close()
    pool.putconn(connection)
    for resource in resources:
        resource_list.append(
            models.Resource(
                resource_id=resource[0],
                name=resource[1],
                path=resource[2],
                size=resource[3]
            )
        )
    return resource_list


def get_resource(resource_id: int) -> Union[models.Resource, None]:
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM resources WHERE id = %s;", (resource_id,))
    resource = cursor.fetchone()
    cursor.close()
    pool.putconn(connection)
    if not resource:
        return None
    return models.Resource(
        resource_id=resource[0],
        name=resource[1],
        path=resource[2],
        size=resource[3]
    )
