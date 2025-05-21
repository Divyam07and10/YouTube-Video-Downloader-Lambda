from utils.helpers import generate_s3_filename
from utils.s3_client import get_s3_client
from core.config import get_settings
from utils.bucket import ensure_bucket_exists

def upload_to_s3(file_path: str, youtube_id: str, format: str = "mp4") -> str:
    settings = get_settings()
    s3_client = get_s3_client()
    bucket_name = settings.S3_BUCKET_NAME
    filename = generate_s3_filename(youtube_id, format)

    try:
        ensure_bucket_exists(s3_client, bucket_name)
        s3_client.upload_file(file_path, bucket_name, filename)
        print(f"Successfully uploaded {file_path} to S3 at {filename}")
        
        if settings.IS_DEVELOPMENT is False:
            s3_url = f"{settings.LOCALSTACK_URL}/{bucket_name}/{filename}"
        else:
            s3_url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
        
        return s3_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        raise
