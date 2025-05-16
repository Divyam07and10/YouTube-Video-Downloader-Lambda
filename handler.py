import json
import os
from utils.youtube import validate_youtube_id, download_youtube_video, extract_metadata
from utils.s3_mock import upload_to_mock_s3
from utils.db import save_video_metadata

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']

def download_video(event, context):
    try:
        method = event.get("httpMethod", "")
        if method == "POST":
            body = json.loads(event.get("body", "{}"))
            youtube_id = body.get("youtube_id")
            format = body.get("format", "mp4")
            quality = body.get("quality", "720p")  # Default to 720p
        elif method == "GET":
            query_params = event.get("queryStringParameters") or {}
            youtube_id = query_params.get("youtube_id")
            format = query_params.get("format", "mp4")
            quality = query_params.get("quality", "720p")  # Default to 720p
        else:
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Unsupported HTTP method"})
            }

        if not youtube_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'youtube_id'"})
            }

        if format not in ALLOWED_FORMATS:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Invalid format. Allowed formats: {ALLOWED_FORMATS}"})
            }

        if quality not in ALLOWED_QUALITIES:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Invalid quality. Allowed qualities: {ALLOWED_QUALITIES}"})
            }

        if not validate_youtube_id(youtube_id):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid YouTube video ID"})
            }

        file_path, info = download_youtube_video(youtube_id, format, quality)
        if not file_path or not os.path.exists(file_path):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to download video or file not found"})
            }

        print(f"Extracting metadata for {file_path}")
        metadata = extract_metadata(file_path, info)
        metadata["youtube_id"] = youtube_id
        metadata["format"] = format
        metadata["quality"] = quality if format != "mp3" else None

        print(f"Uploading to mock S3: {file_path}")
        s3_url = upload_to_mock_s3(file_path, youtube_id, format)
        metadata["s3_url"] = s3_url

        print(f"Saving metadata to database: {metadata}")
        save_video_metadata(metadata)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Video processed successfully",
                "s3_url": s3_url,
                "metadata": metadata
            })
        }

    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }