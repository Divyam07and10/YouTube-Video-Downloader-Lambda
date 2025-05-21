from core.config import get_settings

def get_ydl_format(video_format: str, quality: str) -> str:
    settings = get_settings()
    max_height = settings.quality_map.get(quality, "720")

    if video_format == "mp3":
        return "bestaudio/best"
    elif video_format == "webm":
        return (
            f"bestvideo[vcodec^=vp9][height<={max_height}]+bestaudio[acodec^=opus]/"
            f"bestvideo[height<={max_height}]+bestaudio/best"
        )
    else:
        return f"bestvideo[height<={max_height}]+bestaudio/best"

def get_ydl_options(file_path: str, video_format: str, ydl_format: str) -> dict:
    return {
        "outtmpl": file_path,
        "format": ydl_format,
        "merge_output_format": video_format if video_format != "mp3" else None,
        "ffmpeg_location": "/usr/bin/ffmpeg",
        "postprocessors": [
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": video_format
            } if video_format != "mp3" else {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
        "postprocessor_args": {
            "ffmpeg": [] if video_format in ["mp3", "webm"]
            else ["-c:v", "libx264", "-c:a", "aac", "-strict", "-2"]
        },
        "quiet": False,
        "verbose": True,
        "keepvideo": True
    }
