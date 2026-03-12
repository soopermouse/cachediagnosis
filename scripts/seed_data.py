#!/usr/bin/env python
# cachemed/scripts/seed_data.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.repositories.patient_repo import PatientRepository
from database.repositories.biometric_repo import BiometricRepository
import uuid
import random
from datetime import datetime, timedelta


def seed_patients(count=10):
    """Seed patient data"""
    repo = PatientRepository()

    for i in range(count):
        patient = repo.create({
            'name': f'Patient {i}',
            'email': f'patient{i}@example.com'
        })
        print(f"Created patient: {patient['patientId']}")

        # Seed readings for this patient
        seed_readings(patient['patientId'], random.randint(10, 50))


def seed_readings(patient_id, count=20):
    """Seed biometric readings for a patient"""
    repo = BiometricRepository()

    now = int(datetime.now().timestamp())

    for i in range(count):
        timestamp = now - (i * 3600)  # hours ago

        reading = repo.create({
            'patientId': patient_id,
            'readingType': 'heart_rate',
            'value': {
                'heartRate': random.randint(60, 100)
            }
        })

        print(f"  Created reading: {reading['readingId']}")


if __name__ == '__main__':
    seed_patients(5)