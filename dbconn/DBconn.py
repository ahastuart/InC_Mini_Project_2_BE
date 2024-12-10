import pymysql
from dotenv import load_dotenv
import os

class dbconn:
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            charset=os.getenv('DB_CHARSET'),
            port=int(os.getenv('DB_PORT')),
            autocommit=True         
        )