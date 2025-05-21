from utils.s3_client import get_s3_client

def ensure_bucket_exists(s3_client, bucket_name: str):
    s3_client = get_s3_client()
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except s3_client.exceptions.ClientError:
        s3_client.create_bucket(Bucket=bucket_name)