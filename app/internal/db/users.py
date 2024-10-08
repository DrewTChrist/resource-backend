from typing import Union

from app.internal.db import get_connection_pool
from app.internal import models
from app.internal import hashing


def get_users() -> list[models.User]:
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    user_list = cursor.fetchall()
    return_users = []
    cursor.close()
    pool.putconn(connection)
    for user in user_list:
        return_users.append(
            models.User(
                user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                username=user[3],
                # password [4]
                disabled=user[5],
                admin=user[6],
            )
        )
    return return_users


def get_user(username: str) -> Union[models.UserInDB, None]:
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user = cursor.fetchone()
    cursor.close()
    pool.putconn(connection)
    if not user:
        return None
    return models.UserInDB(
        user_id=user[0],
        first_name=user[1],
        last_name=user[2],
        username=user[3],
        hashed_password=user[4],
        disabled=user[5],
        admin=user[6],
    )


def create_user(user: models.NewUser):
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        (
            "INSERT INTO users"
            " (first_name, last_name, username, password_hash, disabled, administrator)"
            " VALUES (%s, %s, %s, %s, %s, %s);"
        ),
        (
            user.first_name,
            user.last_name,
            user.username,
            hashing.get_password_hash(user.password),
            user.disabled,
            user.admin,
        ),
    )
    connection.commit()
    cursor.close()
    pool.putconn(connection)


def remove_user(user: models.User):
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM users WHERE id = %s AND username = %s;",
        (user.user_id, user.username),
    )
    connection.commit()
    cursor.close()
    pool.putconn(connection)
