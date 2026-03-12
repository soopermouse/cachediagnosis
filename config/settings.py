# cachemed/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # AWS
    AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-1')
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')

    # Database
    DYNAMODB_ENDPOINT = os.environ.get('DYNAMODB_ENDPOINT')

    # Storage
    S3_BUCKET = os.environ.get('S3_BUCKET', f'cachemed-{ENVIRONMENT}-files')

    # Auth
    COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
    COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')

    # API
    PORT = int(os.environ.get('PORT', 5000))

    @classmethod
    def to_dict(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}