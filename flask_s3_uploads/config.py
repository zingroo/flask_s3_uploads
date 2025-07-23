import os

class Config:
    S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_KEY = os.environ.get("S3_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = f'https://{S3_BUCKET}.s3.amazonaws.com/'
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")  # Set a default for dev, override in prod
    DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"
    PORT = int(os.environ.get("PORT", 5000))