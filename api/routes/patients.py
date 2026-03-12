# cachemed/api/routes/patients.py
from flask import request, jsonify
from .. import api_bp
from core.services.patient_service import PatientService

patient_service = PatientService()

@api_bp.route('/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    try:
        data = request.json
        patient = patient_service.create(data)
        return jsonify({'success': True, 'patient': patient}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID"""
    try:
        patient = patient_service.get(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return jsonify({'success': True, 'patient': patient})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient"""
    try:
        data = request.json
        patient = patient_service.update(patient_id, data)
        if not patient:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return jsonify({'success': True, 'patient': patient})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/patients/email/<email>', methods=['GET'])
def get_patient_by_email(email):
    """Get patient by email"""
    try:
        patient = patient_service.get_by_email(email)
        if not patient:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return jsonify({'success': True, 'patient': patient})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500