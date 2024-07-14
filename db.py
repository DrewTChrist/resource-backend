import os
from models import UserInDB
from psycopg2 import pool
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")
print(CONNECTION_STRING)

CONNECTION_POOL = pool.SimpleConnectionPool(1, 10, CONNECTION_STRING)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
        "admin": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
        "admin": False,
    },
    "roberto": {
        "username": "roberto",
        "full_name": "Roberto Garcia",
        "email": "roberto@example.com",
        "hashed_password": "fakehashedsecret3",
        "disabled": False,
        "admin": True,
    },
}


def get_user(username: str):
    connection = CONNECTION_POOL.getconn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    CONNECTION_POOL.putconn(connection)
    return UserInDB(**user)

# def get_user(username: str):
#     if username in db:
#         user_dict = fake_users_db[username]
#         return UserInDB(**user_dict)
