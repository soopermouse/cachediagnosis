# cachemed/storage/s3_client.py
import boto3
import os
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self):
        self.region = os.environ.get('AWS_REGION', 'eu-west-1')
        self.bucket = os.environ.get('S3_BUCKET', 'cachemed-files')
        self.s3 = boto3.client('s3', region_name=self.region)

    def generate_upload_url(self, key, content_type, expires_in=3600):
        """Generate presigned URL for upload"""
        try:
            url = self.s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': key,
                    'ContentType': content_type
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate URL: {e}")

    def generate_download_url(self, key, expires_in=3600):
        """Generate presigned URL for download"""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': key
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate URL: {e}")

    def delete_file(self, key):
        """Delete file from S3"""
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete file: {e}")