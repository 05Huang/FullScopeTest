"""
OSS Upload Utility

Provides a simple interface to upload files to Aliyun OSS.
"""
import os
import uuid
import oss2
from werkzeug.utils import secure_filename
from flask import current_app

def upload_to_oss(file_obj, folder='avatars'):
    """
    Upload a file-like object to Aliyun OSS.
    
    Args:
        file_obj: The file object from Flask request (e.g., request.files['file'])
        folder: The target folder in OSS bucket
        
    Returns:
        tuple: (success, url_or_error_message)
    """
    endpoint = current_app.config.get('OSS_ENDPOINT')
    access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
    access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
    bucket_name = current_app.config.get('OSS_BUCKET_NAME')
    domain = current_app.config.get('OSS_DOMAIN')

    # 添加打印以便排查问题
    print(f"OSS Config - Endpoint: {endpoint}, AccessKeyId: {access_key_id}, AccessKeySecret: {access_key_secret}, BucketName: {bucket_name}")

    # If OSS is not configured, fall back to a dummy success for local dev without OSS
    if not all([endpoint, access_key_id, access_key_secret, bucket_name]):
        return False, "OSS configuration is missing (endpoint, access_key_id, access_key_secret, or bucket_name)"

    try:
        # Secure the filename and generate a unique name to avoid collisions
        original_filename = secure_filename(file_obj.filename)
        ext = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        object_name = f"{folder}/{unique_filename}"

        # Initialize OSS auth and bucket
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        # Upload the file
        file_obj.seek(0)
        bucket.put_object(object_name, file_obj.read())

        # Construct the access URL
        if domain:
            url = f"{domain.rstrip('/')}/{object_name}"
        else:
            # e.g. https://my-bucket.oss-cn-hangzhou.aliyuncs.com/avatars/xxx.png
            protocol = 'https://' if not endpoint.startswith('http') else ''
            endpoint_clean = endpoint.replace('https://', '').replace('http://', '')
            url = f"{protocol}{bucket_name}.{endpoint_clean}/{object_name}"

        return True, url

    except Exception as e:
        return False, f"Failed to upload to OSS: {str(e)}"
