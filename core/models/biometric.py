# cachemed/core/models/biometric.py
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class BiometricReading:
    reading_id: str
    patient_id: str
    reading_type: str
    value: Dict[str, Any]
    timestamp: int
    ttl: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            reading_id=data.get('readingId'),
            patient_id=data.get('patientId'),
            reading_type=data.get('readingType'),
            value=data.get('value', {}),
            timestamp=data.get('timestamp'),
            ttl=data.get('ttl')
        )

    def to_dict(self) -> dict:
        return {
            'readingId': self.reading_id,
            'patientId': self.patient_id,
            'readingType': self.reading_type,
            'value': self.value,
            'timestamp': self.timestamp
        }