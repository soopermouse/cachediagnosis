# cachemed/core/services/patient_service.py
from database.repositories.patient_repo import PatientRepository


class PatientService:
    def __init__(self):
        self.repo = PatientRepository()

    def create(self, data):
        return self.repo.create(data)

    def get(self, patient_id):
        return self.repo.get(patient_id)

    def get_by_email(self, email):
        return self.repo.get_by_email(email)

    def update(self, patient_id, data):
        return self.repo.update(patient_id, data)