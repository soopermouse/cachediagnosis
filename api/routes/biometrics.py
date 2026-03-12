# cachemed/api/routes/biometrics.py
from flask import request, jsonify
from .. import api_bp
from core.services.biometric_service import BiometricService

biometric_service = BiometricService()


@api_bp.route('/biometrics', methods=['POST'])
def add_biometric():
    """Add a biometric reading"""
    try:
        data = request.json
        reading = biometric_service.add(data)
        return jsonify({'success': True, 'reading': reading}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/biometrics/<patient_id>', methods=['GET'])
def get_biometrics(patient_id):
    """Get biometric readings for a patient"""
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        limit = request.args.get('limit', 100)

        readings = biometric_service.get_for_patient(
            patient_id,
            int(start) if start else None,
            int(end) if end else None,
            int(limit)
        )
        return jsonify({'success': True, 'readings': readings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/biometrics/<reading_id>', methods=['DELETE'])
def delete_reading(reading_id):
    """Delete a biometric reading"""
    try:
        biometric_service.delete(reading_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500