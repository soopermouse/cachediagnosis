# cachemed/database/repositories/patient_repo.py
import uuid
from datetime import datetime
from ..client import DatabaseClient


class PatientRepository(DatabaseClient):

    def create(self, data):
        table = self._get_table('patients')
        patient_id = str(uuid.uuid4())
        now = int(datetime.now().timestamp())

        item = {
            'patientId': patient_id,
            'createdAt': now,
            'updatedAt': now,
            'name': data.get('name'),
            'email': data.get('email'),
            'dateOfBirth': data.get('dateOfBirth'),
            'providerId': data.get('providerId', 'unknown')
        }

        item = self._prepare_item(item)
        table.put_item(Item=item)
        return self._from_dynamo(item)

    def get(self, patient_id):
        table = self._get_table('patients')
        response = table.get_item(Key={'patientId': patient_id})
        item = response.get('Item')
        return self._from_dynamo(item) if item else None

    def get_by_email(self, email):
        table = self._get_table('patients')
        from boto3.dynamodb.conditions import Key

        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response.get('Items', [])
        return self._from_dynamo(items[0]) if items else None

    def update(self, patient_id, updates):
        current = self.get(patient_id)
        if not current:
            return None

        table = self._get_table('patients')
        update_expr = []
        expr_attr_values = {}
        expr_attr_names = {}

        for key, value in updates.items():
            if key not in ['patientId', 'createdAt']:
                update_expr.append(f'#{key} = :{key}')
                expr_attr_names[f'#{key}'] = key
                expr_attr_values[f':{key}'] = self._prepare_item(value)

        if not update_expr:
            return current

        now = int(datetime.now().timestamp())
        update_expr.append('#updatedAt = :updatedAt')
        expr_attr_names['#updatedAt'] = 'updatedAt'
        expr_attr_values[':updatedAt'] = now

        response = table.update_item(
            Key={'patientId': patient_id},
            UpdateExpression='SET ' + ', '.join(update_expr),
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues='ALL_NEW'
        )

        return self._from_dynamo(response.get('Attributes'))