import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

CONNECTION_STRING = os.getenv("db_url")


def create_table():
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, first_name TEXT NOT NULL);")
    connection.commit()
    cursor.close()
    connection.close()


create_table()
