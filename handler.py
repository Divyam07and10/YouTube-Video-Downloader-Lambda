import json
import os
from utils.validators import validate_request, ValidationError
from services.youtube import download_youtube_video
from services.metadata import extract_metadata
from utils.s3 import upload_to_s3
from db.save_metadata import save_video_metadata
from utils.helpers import delete_local_file

def download_video(event, context):
    try:
        # Validate and extract parameters
        validated_data = validate_request(event)
        youtube_id = validated_data["youtube_id"]
        video_format = validated_data["format"]
        quality = validated_data["quality"]

        # Download the video
        temporary_file, info = download_youtube_video(youtube_id, video_format, quality)
        if not temporary_file or not os.path.exists(temporary_file):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to download video or file not found"})
            }

        # Extract metadata
        metadata = extract_metadata(temporary_file, info)
        metadata.update({
            "youtube_id": youtube_id,
            "format": video_format,
            "quality": quality if video_format != "mp3" else None,
        })

        # Upload to S3
        s3_url = upload_to_s3(temporary_file, youtube_id, video_format)
        metadata["s3_url"] = s3_url

        # Save to database
        save_video_metadata(metadata)
        
        # Clean up the temporary file
        delete_local_file(temporary_file)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Video processed successfully",
                "s3_url": s3_url,
                "metadata": metadata
            })
        }

    except ValidationError as ve:
        return {
            "statusCode": ve.status_code,
            "body": json.dumps({"error": ve.message})
        }
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }