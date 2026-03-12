# cachemed/core/services/biometric_service.py
from database.repositories.biometric_repo import BiometricRepository


class BiometricService:
    def __init__(self):
        self.repo = BiometricRepository()

    def add(self, data):
        return self.repo.create(data)

    def get_for_patient(self, patient_id, start=None, end=None, limit=100):
        return self.repo.get_for_patient(patient_id, start, end, limit)

    def delete(self, reading_id):
        return self.repo.delete(reading_id)