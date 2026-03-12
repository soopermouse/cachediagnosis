# cachemed/tests/test_api/test_predictions.py
import pytest
import json


def test_generate_prediction(client, sample_patient, sample_readings):
    """Test generating prediction"""
    response = client.post(f"/api/predict/{sample_patient['patientId']}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'prediction' in data


def test_get_predictions(client, sample_patient):
    """Test getting prediction history"""
    response = client.get(f"/api/predictions/{sample_patient['patientId']}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert isinstance(data['predictions'], list)