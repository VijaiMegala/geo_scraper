import os

DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME", "geospatial_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "psql369"),
    "host": os.getenv("DB_HOST", "192.168.0.101"), 
    "port": os.getenv("DB_PORT", "5431"),
}