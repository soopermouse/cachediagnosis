# cachemed/tests/test_api/test_patients.py
import pytest
import json


def test_create_patient(client):
    """Test patient creation"""
    response = client.post('/api/patients', json={
        'name': 'Test Patient',
        'email': 'test@example.com',
        'dateOfBirth': '1980-01-01'
    })

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'patient' in data


def test_get_patient(client, sample_patient):
    """Test getting patient by ID"""
    response = client.get(f"/api/patients/{sample_patient['patientId']}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['patient']['patientId'] == sample_patient['patientId']


def test_get_patient_not_found(client):
    """Test getting non-existent patient"""
    response = client.get('/api/patients/nonexistent')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False