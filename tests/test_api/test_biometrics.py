# cachemed/tests/test_api/test_biometrics.py
import pytest
import json


def test_add_biometric(client, sample_patient):
    """Test adding biometric reading"""
    response = client.post('/api/biometrics', json={
        'patientId': sample_patient['patientId'],
        'readingType': 'heart_rate',
        'value': {'heartRate': 75}
    })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'reading' in data


def test_get_biometrics(client, sample_patient, sample_readings):
    """Test getting biometric readings"""
    response = client.get(f"/api/biometrics/{sample_patient['patientId']}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert isinstance(data['readings'], list)