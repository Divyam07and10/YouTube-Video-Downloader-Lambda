import os
import yt_dlp
from pytube import YouTube
from yt_dlp.utils import DownloadError

def validate_youtube_id(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except DownloadError:
        try:
            YouTube(f"https://www.youtube.com/watch?v={video_id}").check_availability()
            return True
        except:
            return False

def download_youtube_video(video_id, format="mp4", quality="720p"):
    url = f"https://www.youtube.com/watch?v={video_id}"
    file_path = f"/tmp/{video_id}.{format}"
    try:
        # Map quality to yt_dlp resolution syntax
        quality_map = {
            '360p': '360',
            '480p': '480',
            '720p': '720',
            '1080p': '1080',
            '4k': '2160'
        }
        ydl_format = "bestaudio/best" if format == "mp3" else \
                    f"bestvideo[vcodec^=vp9][height<={quality_map[quality]}]+bestaudio[acodec^=opus]/bestvideo[height<={quality_map[quality]}]+bestaudio/best" if format == "webm" else \
                    f"bestvideo[height<={quality_map[quality]}]+bestaudio/best"
        
        ydl_opts = {
            "outtmpl": file_path,
            "format": ydl_format,
            "merge_output_format": format if format != "mp3" else None,
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "postprocessors": [
                {
                    "key": "FFmpegVideoRemuxer",
                    "preferedformat": format
                } if format != "mp3" else {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ],
            "postprocessor_args": {
                "ffmpeg": [] if format in ["mp3", "webm"] else ["-c:v", "libx264", "-c:a", "aac", "-strict", "-2"]
            },
            "quiet": False,
            "verbose": True,
            "keepvideo": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} not created")
                return None, None
            return file_path, info
    except DownloadError as de:
        print(f"yt_dlp DownloadError: {str(de)}")
        try:
            yt = YouTube(url)
            if format == "mp3":
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension=format, resolution=quality).order_by("resolution").desc().first()
            if not stream:
                print(f"Error: No suitable stream found for format {format} and quality {quality}")
                return None, None
            stream.download(output_path="/tmp", filename=f"{video_id}.{format}")
            if not os.path.exists(file_path):
                print(f"Error: pytube file {file_path} not created")
                return None, None
            return file_path, {"title": yt.title, "duration": yt.length, "resolution": stream.resolution if format != "mp3" else "audio"}
        except Exception as e:
            print(f"pytube Error: {str(e)}")
            return None, None
    except Exception as e:
        print(f"Unexpected error in yt_dlp: {str(e)}")
        return None, None

def extract_metadata(file_path, info=None):
    from os.path import getsize, basename
    if not info or not os.path.exists(file_path):
        return {
            "title": basename(file_path) if os.path.exists(file_path) else "unknown",
            "duration": 0,
            "resolution": "unknown",
            "size_bytes": getsize(file_path) if os.path.exists(file_path) else 0
        }
    return {
        "title": info.get("title", basename(file_path)),
        "duration": info.get("duration", 0) or info.get("length", 0),
        "resolution": info.get("resolution", f"{info.get('width', 'unknown')}x{info.get('height', 'unknown')}" if "audio" not in file_path else "audio"),
        "size_bytes": getsize(file_path)
    }