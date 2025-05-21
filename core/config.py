import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings:
    ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
    ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']
    quality_map = {
        '360p': '360',
        '480p': '480',
        '720p': '720',
        '1080p': '1080',
        '4k': '2160'
    }
    
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "youtube-downloader-bucket")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    
    LOCALSTACK_URL = 'http://localhost:4566'
    IS_DEVELOPMENT = os.getenv("IS_DEVELOPMENT", "False")
    if IS_DEVELOPMENT == "False":
        IS_DEVELOPMENT = False
    else:
        IS_DEVELOPMENT = True

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
@lru_cache()
def get_settings():
    return Settings()
