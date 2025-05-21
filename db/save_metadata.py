from db.connection import get_connection
import uuid
from datetime import datetime

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