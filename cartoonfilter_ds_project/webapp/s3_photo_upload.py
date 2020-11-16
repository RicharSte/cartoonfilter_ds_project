from webapp.config import AWS_ACCESS_KEY, AWS_SECRET_KEY

import boto3
import os

def download_photo_s3(file, username, photo_number):
    client = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY)
    
    upload_file_bucket = 'users-photo-1'
    upload_file_key = username + '/' + photo_number
    client.upload_fileobj(file, upload_file_bucket, upload_file_key)