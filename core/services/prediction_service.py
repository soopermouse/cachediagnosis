# cachemed/core/services/prediction_service.py
from database.repositories.prediction_repo import PredictionRepository
from database.repositories.biometric_repo import BiometricRepository
from ml.model import CachemedFusionModel


class PredictionService:
    def __init__(self):
        self.pred_repo = PredictionRepository()
        self.bio_repo = BiometricRepository()
        self.model = CachemedFusionModel()

    def generate(self, patient_id):
        # Get recent readings
        readings = self.bio_repo.get_for_patient(patient_id, limit=100)

        if not readings:
            raise ValueError("No readings found for patient")

        # Generate prediction
        prediction = self.model.predict(readings)

        # Save prediction
        saved = self.pred_repo.create(patient_id, prediction)

        return saved

    def get_history(self, patient_id):
        return self.pred_repo.get_for_patient(patient_id)