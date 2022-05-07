from conf.config import CONFIG
from utils.sql_builder import SQLBuilder


class Cal():

    def __init__(self) -> None:
        pass

if __name__=="__main__":
    builder = SQLBuilder()
    b = builder.create_server_connection()
