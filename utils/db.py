import os
import psycopg2
import uuid
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS videos (
        id UUID PRIMARY KEY,
        youtube_id TEXT NOT NULL,
        title TEXT,
        duration INTEGER,
        resolution TEXT,
        s3_url TEXT NOT NULL,
        format TEXT,
        quality TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    cursor.close()
    conn.close()

def save_video_metadata(meta):
    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO videos (id, youtube_id, title, duration, resolution, s3_url, format, quality, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.execute(insert_sql, (
        str(uuid.uuid4()),
        meta.get("youtube_id"),
        meta.get("title"),
        meta.get("duration"),
        meta.get("resolution"),
        meta.get("s3_url"),
        meta.get("format"),
        meta.get("quality"),
        datetime.utcnow()
    ))

    conn.commit()
    cursor.close()
    conn.close()