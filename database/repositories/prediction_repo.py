# cachemed/database/repositories/prediction_repo.py
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from ..client import DatabaseClient


class PredictionRepository(DatabaseClient):

    def create(self, patient_id, prediction_data):
        table = self._get_table('predictions')
        pred_id = str(uuid.uuid4())
        now = int(datetime.now().timestamp())

        # Determine risk level
        risk_level = prediction_data.get('risk_level', 'unknown')

        item = {
            'predictionId': pred_id,
            'patientId': patient_id,
            'timestamp': now,
            'riskLevel': risk_level,
            'prediction': prediction_data,
            'ttl': now + (30 * 24 * 60 * 60)
        }

        item = self._prepare_item(item)
        table.put_item(Item=item)
        return self._from_dynamo(item)

    def get_for_patient(self, patient_id, limit=50):
        table = self._get_table('predictions')

        response = table.query(
            IndexName='patient-predictions-index',
            KeyConditionExpression=Key('patientId').eq(patient_id),
            Limit=limit,
            ScanIndexForward=False
        )

        items = response.get('Items', [])
        return [self._from_dynamo(item) for item in items]

    def get_latest(self, patient_id):
        predictions = self.get_for_patient(patient_id, limit=1)
        return predictions[0] if predictions else None