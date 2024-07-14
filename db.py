import os
from psycopg2 import pool
from dotenv import load_dotenv
import models
import hashing

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")

CONNECTION_POOL = pool.SimpleConnectionPool(1, 10, CONNECTION_STRING)


def get_user(username: str):
    connection = CONNECTION_POOL.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    CONNECTION_POOL.putconn(connection)
    return models.UserInDB(
        first_name=user[1],
        last_name=user[2],
        username=user[3],
        hashed_password=user[4],
        disabled=user[5],
        admin=user[6]
    )

def create_user(user: models.NewUser):
    connection = CONNECTION_POOL.getconn()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, username, password_hash, disabled, administrator) VALUES (%s, %s, %s, %s, %s, %s)", 
        (
            user.first_name, # first_name
            user.last_name, # last_name
            user.username, # username
            hashing.get_password_hash(user.password), # password
            user.disabled, # disabled
            user.admin # admin
        )
    )
    connection.commit()
    cursor.close()
    CONNECTION_POOL.putconn(connection)
