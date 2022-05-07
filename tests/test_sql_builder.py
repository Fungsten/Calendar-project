from utils.sql_builder import SQLBuilder

def test_create_server_connection():
    server = SQLBuilder()
    assert server.create_server_connection() is not None

def test_create_db_connection():
    server = SQLBuilder()
    c = server.create_server_connection()
    server.create_database(c, 'test')
    assert server.create_db_connection('test') is not None
    assert server.create_db_connection('potato') is None