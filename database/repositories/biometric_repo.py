# cachemed/database/repositories/biometric_repo.py
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from ..client import DatabaseClient


class BiometricRepository(DatabaseClient):

    def create(self, data):
        table = self._get_table('biometrics')
        reading_id = str(uuid.uuid4())
        now = int(datetime.now().timestamp())

        item = {
            'patientId': data['patientId'],
            'timestamp': now,
            'readingId': reading_id,
            'readingType': data.get('readingType', 'unknown'),
            'value': data.get('value', {}),
            'ttl': now + (30 * 24 * 60 * 60)
        }

        item = self._prepare_item(item)
        table.put_item(Item=item)
        return self._from_dynamo(item)

    def get_for_patient(self, patient_id, start=None, end=None, limit=100):
        table = self._get_table('biometrics')

        if not start:
            start = 0
        if not end:
            end = int(datetime.now().timestamp())

        response = table.query(
            KeyConditionExpression=
            Key('patientId').eq(patient_id) &
            Key('timestamp').between(start, end),
            Limit=limit,
            ScanIndexForward=False
        )

        items = response.get('Items', [])
        return [self._from_dynamo(item) for item in items]

    def delete(self, reading_id):
        # Need patientId as well for key
        # This is simplified - in practice you'd need both keys
        table = self._get_table('biometrics')
        # You'd need to query for the item first to get patientId
        return {'success': False, 'error': 'Not implemented - requires patientId'}