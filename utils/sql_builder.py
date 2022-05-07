import json
from typing import List

import mysql.connector
import pandas as pd
from conf.config import CONFIG
from mysql.connector import Error


class SQLBuilder():

    def __init__(self) -> None:
        self.host_name = CONFIG.get("host")
        self.user = CONFIG.get("root_user")
        self.password = CONFIG.get("password")

        self.event_headers = CONFIG.get("event_headers")
        self.person_headers = CONFIG.get("person_headers")

        self.person_count = 0
        self.event_count = 0

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

    def create_database(self, connection, db: str):
        cursor = connection.cursor()
        query = f"CREATE DATABASE {db}"
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

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
            return False
        return True

    def execute_query_result(self, connection, query: str):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except Error as err:
            print(f"Error: '{err}'")

        return result

    def hard_reset(self, connection, db):
        query = f"DROP DATABASE {db}"
        self.execute_query(connection, query)

    def load_person_into_pd(self, results):
        from_db = []
        for result in results:
            result = list(result)
            from_db.append(result)
        df = pd.DataFrame(from_db, columns=self.person_headers)
        return df

    def load_event_into_pd(self, results):
        from_db = []
        for result in results:
            result = list(result)
            from_db.append(result)
        df = pd.DataFrame(from_db, columns=self.event_headers)
        return df

    def df_to_json(self, df):
        parsed_json = json.loads(df.to_json(orient="index"))
        return json.dumps(parsed_json, indent=4)

    def read_all_from_table(self, connection, table: str):
        query = f"SELECT * FROM {table}"
        return self.execute_query_result(connection, query)

    def read_from_table_by_id(self, connection, table: str, id: str):
        query = f"SELECT * FROM {table} where {table}_id={id}"
        return self.execute_query_result(connection, query)

    def add_person(self, connection, name, email):
        query = f'''
        INSERT INTO person VALUES
        ({self.person_count + 1}, {name}, {email});
        '''
        if self.execute_query(connection, query):
            self.person_count += 1

    def add_event(self, connection, 
                    name: str, 
                    location: str, 
                    start_time, 
                    end_time, 
                    is_all_day: bool,
                    participants: List[int]):
        query = f'''
        INSERT INTO event VALUES
        ({self.event_count + 1}, {name}, {location}, {start_time}, {end_time}, {is_all_day});
        '''
        if self.execute_query(connection, query):
            self.event_count += 1

        for participant in participants:
            add_participant = f'''
            INSERT INTO participate_event
            ({participant}, {self.event_count})
            '''
            self.execute_query(connection, add_participant)
