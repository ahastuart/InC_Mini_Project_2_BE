import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET'),
    'port': int(os.getenv('DB_PORT')),
    'autocommit': True
}


def test_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("Database connection successful!")
        conn.close()
        return True
    except pymysql.Error as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()