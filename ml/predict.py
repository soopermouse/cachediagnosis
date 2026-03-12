# cachemed/ml/predict.py
import numpy as np
from typing import Dict, List
from .features import extract_features
from .model import CachemedFusionModel

_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = CachemedFusionModel()
    return _model_instance

def predict(readings: List[Dict]) -> Dict:
    """Make prediction from readings"""
    model = get_model()
    return model.predict(readings)

def batch_predict(patients_readings: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """Make predictions for multiple patients"""
    results = {}
    for patient_id, readings in patients_readings.items():
        results[patient_id] = predict(readings)
    return results