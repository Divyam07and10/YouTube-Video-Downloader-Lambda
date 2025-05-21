from services.yt_dlp import download_with_yt_dlp
from services.pytube import download_with_pytube
from services.metadata import extract_metadata

def download_youtube_video(video_id, format="mp4", quality="720p"):
    try:
        temporary_file, info = download_with_yt_dlp(video_id, format, quality)
        if not temporary_file:
            temporary_file, info = download_with_pytube(video_id, format, quality)
        return temporary_file, extract_metadata(temporary_file, info)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, None
