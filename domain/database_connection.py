from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:
    """It enables connection with database and execute queries."""

    # Connection Parameters for MySql DB
    _USERNAME = 'root'
    _PASSWORD = 'root'
    _DATABASE_NAME = 'zsi_project_db'
    _SERVER_HOST = 'localhost'
    _SERVER_PORT = '3306'
    # MySQL-Connector-Python
    _DATABASE_URI = f'mysql+mysqlconnector://{_USERNAME}:{_PASSWORD}@{_SERVER_HOST}:{_SERVER_PORT}/{_DATABASE_NAME}'

    def __init__(self):
        self._engine = create_engine(self._DATABASE_URI, echo=False, pool_size=20, max_overflow=0)

    def get_connection_to_database(self):
        return self._engine.connect()

    def get_engine(self):
        return self._engine

    def get_cursor(self):
        """The cursor is used to execute raw queries to database."""
        connection = self._engine.raw_connection()
        return connection.cursor()

    def create_session(self):
        """The session allows you using built-in functions to execute queries to database."""
        Session = sessionmaker(bind=self._engine)
        return Session()

