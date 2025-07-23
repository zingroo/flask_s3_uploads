from flask import Flask, render_template, request, jsonify
import os, boto3
from botocore.client import Config

app = Flask(__name__)

@app.route("/account/", methods=['GET', 'POST'])
def account():
    return render_template('account.html')

@app.route('/sign-s3/', methods=['GET', 'POST'])
def sign_s3():
    s3_bucket = os.environ.get('S3_BUCKET')
    s3_key = os.environ.get('S3_KEY')
    s3_secret = os.environ.get('S3_SECRET_ACCESS_KEY')
    file_name = request.args.get('file-name')
    file_type = request.args.get('file-type')

    # Input validation
    if not file_name or not file_type:
        return jsonify({'error': 'Missing file-name or file-type parameter.'}), 400
    if '/' in file_name or '\\' in file_name:
        return jsonify({'error': 'Invalid file name.'}), 400

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=s3_key,
            aws_secret_access_key=s3_secret,
            config=Config(signature_version='s3v4')
        )

        presigned_post = s3.generate_presigned_post(
            Bucket=s3_bucket,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )

        return jsonify({
            'data': presigned_post,
            'url': f'https://{s3_bucket}.s3.amazonaws.com/{file_name}',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
