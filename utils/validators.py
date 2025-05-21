from utils.helpers import get_youtube_url
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from pytube import YouTube
import json
from core.config import get_settings

class ValidationError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def validate_request(event: dict) -> dict:
    method = event.get("httpMethod", "")
    if method not in ("GET", "POST"):
        raise ValidationError("Unsupported HTTP method", status_code=405)
    
    if method == "POST":
        body = event.get("body")
        try:
            data = json.loads(body or "{}")
        except Exception:
            raise ValidationError("Invalid JSON body")
    else:
        data = event.get("queryStringParameters") or {}

    youtube_id = data.get("youtube_id")
    video_format = data.get("format", "mp4")
    quality = data.get("quality", "720p")

    if not youtube_id:
        raise ValidationError("Missing 'youtube_id'")

    settings = get_settings()

    if video_format not in settings.ALLOWED_FORMATS:
        raise ValidationError(f"Invalid format. Allowed formats: {settings.ALLOWED_FORMATS}")

    if quality not in settings.ALLOWED_QUALITIES:
        raise ValidationError(f"Invalid quality. Allowed qualities: {settings.ALLOWED_QUALITIES}")

    if not validate_youtube_id(youtube_id):
        raise ValidationError("Invalid YouTube video ID")

    return {
        "youtube_id": youtube_id,
        "format": video_format,
        "quality": quality,
    }
    
def validate_youtube_id(video_id: str) -> bool:
    url = get_youtube_url(video_id)
    try:
        with YoutubeDL({"quiet": True}) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except DownloadError:
        try:
            YouTube(url).check_availability()
            return True
        except Exception:
            return False
