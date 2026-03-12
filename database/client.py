# cachemed/database/client.py
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import uuid
from datetime import datetime
import os
from typing import Dict, List, Optional, Any


class DatabaseClient:
    """Main database client"""

    def __init__(self):
        self.env = os.environ.get('ENVIRONMENT', 'dev')
        self.region = os.environ.get('AWS_REGION', 'eu-west-1')
        self.endpoint = os.environ.get('DYNAMODB_ENDPOINT', None)

        if self.endpoint:
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region, endpoint_url=self.endpoint)
        else:
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region)

    def _get_table(self, name):
        return self.dynamodb.Table(f'cachemed-{self.env}-{name}')

    def _prepare_item(self, item):
        """Prepare item for DynamoDB"""
        if isinstance(item, dict):
            return {k: self._prepare_item(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._prepare_item(i) for i in item]
        elif isinstance(item, float):
            return Decimal(str(item))
        else:
            return item

    def _from_dynamo(self, item):
        """Convert DynamoDB item to Python"""
        if isinstance(item, dict):
            return {k: self._from_dynamo(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._from_dynamo(i) for i in item]
        elif isinstance(item, Decimal):
            return float(item) if item % 1 else int(item)
        else:
            return item