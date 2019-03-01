from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_assets import Environment, Bundle
import os, json, boto3, botocore
from botocore.client import Config
from config import *
from helpers import *

app = Flask(__name__)


# Listen for GET requests to yourdomain.com/account/
@app.route("/account/", methods = ['GET' , 'POST'])
def account():
  # Show the account-edit HTML page:
  return render_template('account.html')



@app.route('/sign-s3/', methods = ['GET' , 'POST'])
def sign_s3():

  # Load necessary information into the application
  S3_BUCKET = os.environ.get('S3_BUCKET')
  S3_KEY = os.environ.get("S3_KEY")
  S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
  # print("************KEY AND SECRET***********")
  # print(S3_KEY)
  # print(S3_SECRET)

  file_name = request.args.get('file-name')
  file_type = request.args.get('file-type')

  
  
  

  # Initialise the S3 client

  s3 = boto3.client('s3',
       aws_access_key_id=S3_KEY,
       aws_secret_access_key=S3_SECRET,
       # region_name = '',
       config=Config(signature_version='s3v4')
    )
   dynamodb = boto3.resource('dynamodb',
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET,
        region_name = 'us-east-1',
        config=Config(signature_version='s3v4')
        )




  # Generate and return the presigned URL
  presigned_post = s3.generate_presigned_post( Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
       {"acl": "public-read"},
        {"Content-Type": file_type}
     ],

    
    ExpiresIn = 3600
  )
  
   table = dynamodb.Table('s3image')

   table.put_item(Item={'url':'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)})


  # Return the data to the client
  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name),
    
  })





# Main code
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
  port = int(os.environ.get('PORT', 5000))
