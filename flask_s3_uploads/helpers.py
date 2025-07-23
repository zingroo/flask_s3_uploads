import boto3
from config import Config

def get_s3_client():
    """Return a boto3 S3 client using credentials from config."""
    return boto3.client(
        's3',
        aws_access_key_id=Config.S3_KEY,
        aws_secret_access_key=Config.S3_SECRET
    )







