import os
from yt_dlp import YoutubeDL
from utils.helpers import get_youtube_url, get_temporary_download_file_path
from utils.yt_dlp_utils import get_ydl_format, get_ydl_options

def download_with_yt_dlp(video_id: str, format: str = "mp4", quality: str = "720p"):
    url = get_youtube_url(video_id)
    file_path = get_temporary_download_file_path(video_id, format)
    
    ydl_format = get_ydl_format(format, quality)
    ydl_opts = get_ydl_options(file_path, format, ydl_format)

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not created")
            return None, None
        return file_path, info
