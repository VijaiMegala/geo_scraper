from psycopg2 import pool, OperationalError, DatabaseError
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_CONFIG

class DatabaseConnection:
    _instance = None
    _pool = None

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection._instance = DatabaseConnection()
        return DatabaseConnection._instance

    def __init__(self):
        if DatabaseConnection._pool is None:
            try:
                DatabaseConnection._pool = pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,  
                    **DATABASE_CONFIG
                )
            except OperationalError as e:
                raise Exception(f"Failed to initialize connection pool: {e}")

    def get_connection(self):
        if DatabaseConnection._pool:
            try:
                return DatabaseConnection._pool.getconn()
            except DatabaseError as e:
                raise Exception(f"Failed to get connection from pool: {e}")
        else:
            raise Exception("Connection pool is not initialized.")

    def release_connection(self, conn):
        if DatabaseConnection._pool:
            try:
                DatabaseConnection._pool.putconn(conn)
            except DatabaseError as e:
                raise Exception(f"Failed to release connection back to pool: {e}")

    def close_all_connections(self):
        if DatabaseConnection._pool:
            try:
                DatabaseConnection._pool.closeall()
            except DatabaseError as e:
                raise Exception(f"Failed to close all connections in pool: {e}")
