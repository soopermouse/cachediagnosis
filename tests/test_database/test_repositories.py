# cachemed/tests/test_database/test_repositories.py
import pytest
from database.repositories.patient_repo import PatientRepository


def test_patient_repo_create(mock_dynamodb):
    """Test patient repository create"""
    repo = PatientRepository()

    data = {
        'name': 'Test Patient',
        'email': 'test@example.com'
    }

    patient = repo.create(data)
    assert patient['name'] == 'Test Patient'
    assert patient['email'] == 'test@example.com'
    assert 'patientId' in patient


def test_patient_repo_get(mock_dynamodb, sample_patient):
    """Test patient repository get"""
    repo = PatientRepository()

    patient = repo.get(sample_patient['patientId'])
    assert patient is not None
    assert patient['patientId'] == sample_patient['patientId']