import boto3

from src.config import Config

_s3_client = None

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client =  boto3.client(
            's3',
            endpoint_url=Config.CLOUDFLARE_R2_ENDPOINT,
            aws_access_key_id=Config.CLOUDFLARE_R2_ACCESS_KEY_ID,
            aws_secret_access_key=Config.CLOUDFLARE_R2_SECRET_ACCESS_KEY
        )
    
    return _s3_client


def upload_file(local_path, destination_key):
    s3 = get_s3_client()

    s3.upload_file(
        Filename=local_path,
        Bucket=Config.CLOUDFLARE_BUCKET_NAME,
        Key=destination_key
    )

    print(f"[Storage] Uploaded {local_path} to {destination_key}")