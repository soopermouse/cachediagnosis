# cachemed/auth/cognito.py
import boto3
import os
from botocore.exceptions import ClientError


class CognitoAuth:
    def __init__(self):
        self.region = os.environ.get('AWS_REGION', 'eu-west-1')
        self.user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        self.client_id = os.environ.get('COGNITO_CLIENT_ID')

        self.client = boto3.client('cognito-idp', region_name=self.region)

    def verify_token(self, token):
        """Verify a Cognito token"""
        try:
            response = self.client.get_user(
                AccessToken=token
            )
            return response
        except ClientError as e:
            return None

    def get_user_from_token(self, token):
        """Extract user info from token"""
        response = self.verify_token(token)
        if not response:
            return None

        user_data = {}
        for attr in response.get('UserAttributes', []):
            user_data[attr['Name']] = attr['Value']

        return {
            'username': response.get('Username'),
            'email': user_data.get('email'),
            'sub': user_data.get('sub')
        }