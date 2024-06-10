import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

key = os.getenv("SECRET_KEY_DATABASE")
user = os.getenv("USER_DATABASE")

def get_db_connection():
    conn = psycopg2.connect(database="bdd_postgres",
                            host="localhost",
                            user=user,
                            password=key,
                            port="5432")
    cursor = conn.cursor()
    return cursor

def release_db_connection(conn):
    conn.close()