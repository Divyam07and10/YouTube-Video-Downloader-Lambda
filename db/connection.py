import psycopg2
from core.config import get_settings

settings = get_settings()

def get_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
    except psycopg2.Error as e:
        raise ConnectionError(f"Database connection error: {str(e)}")
