import mysql.connector
from mysql.connector import Error

from conf.config import CONFIG

class SQLBuilder():

    def __init__(self) -> None:
        self.host_name = CONFIG.get("host")
        self.user = CONFIG.get("root_user")
        self.password = CONFIG.get("password")


    def create_server_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = self.host_name,
                user = self.user,
                passwd = self.password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection

    def create_database(self, connection, query: str):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    def create_db_connection(self, db_name: str):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = self.host_name,
                user = self.user,
                passwd = self.password,
                database=db_name
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
