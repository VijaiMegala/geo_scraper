import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_CONFIG

def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
