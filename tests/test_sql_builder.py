from utils.sql_builder import SQLBuilder

def test_create_server_connection():
    server = SQLBuilder()
    assert server.create_server_connection() is not None
