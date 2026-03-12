# cachemed/tests/test_core/test_models.py
from core.models.patient import Patient


def test_patient_from_dict():
    """Test patient model creation from dict"""
    data = {
        'patientId': '123',
        'name': 'Test Patient',
        'email': 'test@example.com'
    }

    patient = Patient.from_dict(data)
    assert patient.patient_id == '123'
    assert patient.name == 'Test Patient'
    assert patient.email == 'test@example.com'


def test_patient_to_dict():
    """Test patient model conversion to dict"""
    patient = Patient(
        patient_id='123',
        name='Test Patient',
        email='test@example.com'
    )

    data = patient.to_dict()
    assert data['patientId'] == '123'
    assert data['name'] == 'Test Patient'
    assert data['email'] == 'test@example.com'