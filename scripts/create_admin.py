#!/usr/bin/env python
# cachemed/scripts/create_admin.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boto3
import os
from getpass import getpass


def create_admin_user(email, password):
    """Create admin user in Cognito"""
    region = os.environ.get('AWS_REGION', 'eu-west-1')
    user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')

    if not user_pool_id:
        print("Error: COGNITO_USER_POOL_ID not set in environment")
        return False

    client = boto3.client('cognito-idp', region_name=region)

    try:
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=email,
            TemporaryPassword=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'},
                {'Name': 'custom:role', 'Value': 'admin'}
            ],
            DesiredDeliveryMediums=['EMAIL']
        )

        print(f"Admin user created: {email}")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


if __name__ == '__main__':
    email = input("Enter admin email: ")
    password = getpass("Enter temporary password: ")

    create_admin_user(email, password)