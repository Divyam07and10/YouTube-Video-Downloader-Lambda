from datetime import datetime
import os

def generate_s3_filename(youtube_id: str, format: str = "mp4") -> str:
    timestamp = datetime.utcnow().isoformat()
    return f"videos/{youtube_id}_{timestamp}.{format}"

def delete_local_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"Temporary local file {file_path} deleted successfully!!!")
    except Exception as e:
        print(f"Warning: Could not delete local file: {e}")

def get_youtube_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"

def get_temporary_download_file_path(video_id: str, format: str = "mp4") -> str:
    return f"/tmp/{video_id}.{format}"