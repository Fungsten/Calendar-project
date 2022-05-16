import json
from typing import Dict, List, Set

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

        self.event_table = CONFIG.get("event_table")
        self.people_table = CONFIG.get("person_table")
        self.participant_table = CONFIG.get("participant_table")

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
            print(f'Executing query: {query}')
            cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
            return False
        return cursor.lastrowid

    def execute_query_result(self, connection, query: str):
        cursor = connection.cursor(dictionary=True)
        result = None
        try:
            print(f'Executing query: {query}')
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

    def read_from_table_by_id(self, connection, table: str, id: str, label: str = None):
        if label:
            query = f"SELECT * FROM {table} where {label}_id={id}"
        else:
            query = f"SELECT * FROM {table} where {table}_id={id}"
        return self.execute_query_result(connection, query)

    def add_person(self, connection, name, email):
        query = f'''
        INSERT INTO person 
        (name, email)
        VALUES (\'{name}\', \'{email}\');
        '''
        self.execute_query(connection, query)

    def add_event(self, connection, 
                    name: str, 
                    location: str, 
                    start_time, 
                    end_time, 
                    is_all_day: bool,
                    participants: List[int]):
        query = f'''
        INSERT INTO event 
        (name, location, start_time, end_time, is_all_day)
        VALUES (\'{name}\', \'{location}\', \'{start_time}\', \'{end_time}\', {is_all_day});
        '''
        id = self.execute_query(connection, query)

        self.add_participants(connection, participants, id)

    def delete_item_by_id(self, connection,
                            id: int,
                            table: str) -> None:
        delete_query = f'''
        DELETE FROM {table}
        WHERE {table}_id = {id};
        '''
        self.execute_query(connection, delete_query)

    def delete_participant(self, connection, person_id: int, event_id: int) -> None:
        delete_query = f'''
        DELETE FROM {self.participant_table}
        WHERE person_id = {person_id} AND event_id = {event_id};
        '''
        self.execute_query(connection, delete_query)

    def add_participants(self, connection, participants: List[int], event_id: int) -> None:
        add_participant = f'''
        INSERT INTO participate_event VALUES
        '''
        for participant in participants:
            add_participant += f'({participant}, {event_id}),'

        self.execute_query(connection, add_participant[:-1])

    def update_item_by_id(self, connection, id: int, table: str, update: Dict[str, str]) -> None:
        if not update or len(update.keys()) < 1:
            return
        update_query = f'''
        UPDATE {table}
        SET
        '''
        for k in update.keys():
            update_query += f'{k} = \'{update.get(k)}\','
        update_query = update_query[:-1] # slice off last comma

        update_query += f'''
        WHERE {table}_id = {id}
        '''
        self.execute_query(connection, update_query)

    def get_event_name(self, connection, event_id: int):
        r = self.read_from_table_by_id(connection, 'event', event_id)
        return r[0].get('name')

    def get_person_email(self, connection, person_id: int):
        r = self.read_from_table_by_id(connection, 'person', person_id)
        return r[0].get('email')

    def get_num_events(self, connection):
        count_query = f'''
        SELECT COUNT(*) FROM {self.event_table}
        '''
        return self.execute_query(connection, count_query)

    def get_num_people(self, connection):
        count_query = f'''
        SELECT COUNT(*) FROM {self.people_table}
        '''
        return self.execute_query(connection, count_query)
