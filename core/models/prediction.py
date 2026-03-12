# cachemed/core/models/prediction.py
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Prediction:
    prediction_id: str
    patient_id: str
    prediction: Dict
    timestamp: int
    ttl: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            prediction_id=data.get('predictionId'),
            patient_id=data.get('patientId'),
            prediction=data.get('prediction', {}),
            timestamp=data.get('timestamp'),
            ttl=data.get('ttl')
        )

    def to_dict(self) -> dict:
        return {
            'predictionId': self.prediction_id,
            'patientId': self.patient_id,
            'prediction': self.prediction,
            'timestamp': self.timestamp
        }
