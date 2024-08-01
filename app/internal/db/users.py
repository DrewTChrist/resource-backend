from app.internal.db import get_connection_pool
from app.internal import configuration
from app.internal import models
from app.internal import hashing


def get_user(username: str):
    pool = get_connection_pool()
    connection = pool.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    pool.putconn(connection)
    return models.UserInDB(
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
        "INSERT INTO users (first_name, last_name, username, password_hash, disabled, administrator) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            user.first_name,  # first_name
            user.last_name,  # last_name
            user.username,  # username
            hashing.get_password_hash(user.password),  # password
            user.disabled,  # disabled
            user.admin,  # admin
        ),
    )
    connection.commit()
    cursor.close()
    pool.putconn(connection)