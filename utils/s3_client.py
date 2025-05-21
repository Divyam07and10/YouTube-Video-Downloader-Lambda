import boto3
from core.config import get_settings

def get_s3_client():
    settings = get_settings()
    client_kwargs = {
        'service_name': 's3',
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
        'region_name': settings.AWS_REGION,
    }
    if settings.IS_DEVELOPMENT == False:
        client_kwargs['endpoint_url'] = settings.LOCALSTACK_URL
    
    return boto3.client(**client_kwargs)