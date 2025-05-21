import os
from os.path import getsize, basename

def extract_metadata(file_path: str, info: dict = None) -> dict:
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
        "resolution": info.get("resolution") or (
            f"{info.get('width', 'unknown')}x{info.get('height', 'unknown')}"
            if "audio" not in file_path else "audio"
        ),
        "size_bytes": getsize(file_path)
    }
