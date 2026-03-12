# cachemed/api/middleware/auth.py
from functools import wraps
from flask import request, jsonify
import os


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'success': False, 'error': 'Token missing'}), 401

        # Simple token validation (replace with real auth)
        if not token.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        # Here you would validate the token with Cognito
        # For now, just pass through
        return f(*args, **kwargs)

    return decorated