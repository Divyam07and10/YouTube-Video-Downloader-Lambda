from pytube import YouTube

def get_stream(yt: YouTube, format: str, quality: str):
    if format == "mp3":
        return yt.streams.filter(only_audio=True).first()
    return yt.streams.filter(
        progressive=True,
        file_extension=format,
        resolution=quality
    ).order_by("resolution").desc().first()