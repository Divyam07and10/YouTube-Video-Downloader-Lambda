import os
from pytube import YouTube
from utils.helpers import get_youtube_url, get_temporary_download_file
from utils.pytube_utils import get_stream

def download_with_pytube(video_id: str, format: str = "mp4", quality: str = "720p"):
    url = get_youtube_url(video_id)
    temporary_file = get_temporary_download_file(video_id, format)
    
    try:
        yt = YouTube(url)
        stream = get_stream(yt, format, quality)
        
        if not stream:
            print(f"Error: No stream available for {format} at {quality}")
            return None, None

        stream.download(output_path="/tmp", filename=f"{video_id}.{format}")

        if not os.path.exists(temporary_file):
            print(f"Error: File {temporary_file} not created")
            return None, None

        metadata = {
            "title": yt.title,
            "duration": yt.length,
            "resolution": stream.resolution if format != "mp3" else "audio"
        }
        
        return temporary_file, metadata
    
    except Exception as e:
        print(f"Download Error: {str(e)}")
        return None, None