# cachemed/api/middleware/validation.py
from functools import wraps
from flask import request, jsonify
import re


def validate_patient_data(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.json
        errors = []

        if not data.get('name'):
            errors.append('name is required')
        if not data.get('email'):
            errors.append('email is required')
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', data.get('email')):
            errors.append('email is invalid')

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        return f(*args, **kwargs)

    return decorated


def validate_biometric_data(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.json
        errors = []

        if not data.get('patientId'):
            errors.append('patientId is required')
        if not data.get('readingType'):
            errors.append('readingType is required')
        if data.get('value') is None:
            errors.append('value is required')

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        return f(*args, **kwargs)

    return decorated