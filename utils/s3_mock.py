import boto3
import os
from datetime import datetime

def upload_to_mock_s3(file_path, youtube_id, format="mp4"):
    # Configure S3 client for LocalStack
    s3_client = boto3.client(
        's3',
        endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT', 'http://localhost:4566'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    # Define bucket name and file key
    BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'youtube-downloader-bucket')
    filename = f"videos/{youtube_id}_{datetime.utcnow().isoformat()}.{format}"
    
    # Define the loLOCALSTACK ENDPOINT
    endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT', 'http://localhost:4566')

    try:
        # Create bucket if it doesn't exist
        try:
            s3_client.head_bucket(Bucket=BUCKET_NAME)
        except s3_client.exceptions.ClientError:
            s3_client.create_bucket(Bucket=BUCKET_NAME)

        # Upload file to S3
        s3_client.upload_file(file_path, BUCKET_NAME, filename)
        
        # Clean up local file
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Warning: Failed to delete local file {file_path}: {str(e)}")

        # Generate S3 URL
        s3_url = f"{endpoint_url}://{BUCKET_NAME}/{filename}"
        return s3_url

    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise