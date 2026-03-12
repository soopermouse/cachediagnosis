# cachemed/database/repositories/file_repo.py
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from ..client import DatabaseClient


class FileRepository(DatabaseClient):

    def create(self, data):
        table = self._get_table('files')
        file_id = str(uuid.uuid4())
        now = int(datetime.now().timestamp())

        item = {
            'fileId': file_id,
            'patientId': data['patientId'],
            'uploadDate': now,
            'filename': data.get('filename'),
            'mimeType': data.get('mimeType'),
            'fileType': data.get('fileType'),
            'storagePath': data.get('storagePath'),
            'status': 'pending',
            'size': data.get('size', 0)
        }

        item = self._prepare_item(item)
        table.put_item(Item=item)
        return self._from_dynamo(item)

    def get(self, file_id):
        table = self._get_table('files')
        response = table.get_item(Key={'fileId': file_id})
        item = response.get('Item')
        return self._from_dynamo(item) if item else None

    def list_for_patient(self, patient_id, limit=100):
        table = self._get_table('files')

        response = table.query(
            IndexName='patient-files-index',
            KeyConditionExpression=Key('patientId').eq(patient_id),
            Limit=limit,
            ScanIndexForward=False
        )

        items = response.get('Items', [])
        return [self._from_dynamo(item) for item in items]

    def update_status(self, file_id, status):
        table = self._get_table('files')

        response = table.update_item(
            Key={'fileId': file_id},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': status},
            ReturnValues='ALL_NEW'
        )

        return self._from_dynamo(response.get('Attributes'))