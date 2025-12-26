import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = pooling.MySQLConnectionPool(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3307)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    auth_plugin="mysql_native_password"
)

def get_connection():
    return db_pool.get_connection()
