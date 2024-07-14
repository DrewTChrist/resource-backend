import os

import bcrypt
from dotenv import load_dotenv
import psycopg2

from models import UserInDB

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")


def get_password_hash(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    hashed_password = hashed_password.decode("utf-8")
    return hashed_password


def create_user():
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, username, password_hash, disabled, administrator) VALUES (%s, %s, %s, %s, %s, %s)", 
        ("Fart", "Wahlberg", "johndoe", get_password_hash("secret"), False, True)
    )
    connection.commit()
    cursor.close()
    connection.close()

create_user()
