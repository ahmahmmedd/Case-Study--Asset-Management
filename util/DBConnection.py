import mysql.connector
from util.DBPropertyUtil import get_db_properties

class DBConnection:
    @staticmethod
    def get_connection():
        db_props = get_db_properties()
        return mysql.connector.connect(
            host=db_props["host"],
            port=db_props["port"],
            user=db_props["user"],
            password=db_props["password"],
            database=db_props["database"]
        )