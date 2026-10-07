import mysql.connector
from config import db_host,db_port,db_user,db_password,db_database_name


def get_connection():
    return mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_database_name,
        )

