import boto3, botocore
from config import *
import json
from flask_cors import CORS , cross_origin

s3 = boto3.client(
	   's3',
	   aws_access_key_id=S3_KEY,
	   aws_secret_access_key=S3_SECRET
	   )







