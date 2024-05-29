from dotenv import load_dotenv
import os

import mysql.connector


load_dotenv()

__key = os.getenv("SECRET_KEY_DATABASE")


cnx = mysql.connector.connect(
    user='root',
    password=__key,
    host='localhost',
    database='dreamhouse'
)
cursor = cnx.cursor()


cursor.execute("select * from client;")

results = cursor.fetchall()

print(results)

cursor.close()
cnx.close()