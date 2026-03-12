# cachemed/core/models/patient.py
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Patient:
    patient_id: str
    name: str
    email: str
    date_of_birth: Optional[str] = None
    provider_id: str = 'unknown'
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            patient_id=data.get('patientId'),
            name=data.get('name'),
            email=data.get('email'),
            date_of_birth=data.get('dateOfBirth'),
            provider_id=data.get('providerId', 'unknown'),
            created_at=data.get('createdAt'),
            updated_at=data.get('updatedAt')
        )

    def to_dict(self) -> dict:
        return {
            'patientId': self.patient_id,
            'name': self.name,
            'email': self.email,
            'dateOfBirth': self.date_of_birth,
            'providerId': self.provider_id,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }