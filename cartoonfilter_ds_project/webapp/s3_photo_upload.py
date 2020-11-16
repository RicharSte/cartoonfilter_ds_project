from webapp.config import AWS_ACCESS_KEY, AWS_SECRET_KEY
from PIL import Image
import boto3
import io
import os

def download_photo_s3(file, username, photo_number):
    client = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY)
    
    cartoonize_image_in_image_format = Image.fromarray(file)
    # change image format to bytes
    image_in_bytes_format = io.BytesIO()
    cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
    image_in_bytes_format = image_in_bytes_format.getvalue()
    # load bytes into ram, so bot can send it
    file = io.BytesIO(image_in_bytes_format)
    
    
    upload_file_bucket = 'users-photo-1'
    upload_file_key = username + '/' + photo_number
    client.upload_fileobj(file, upload_file_bucket, upload_file_key)