from functools import lru_cache
from psycopg2 import pool

from app.internal import configuration


@lru_cache
def get_connection_pool():
    connection_string = configuration.get_config().db_url
    connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)
    return connection_pool
