# cachemed/auth/decorators.py
from functools import wraps
from flask import request, jsonify
from .cognito import CognitoAuth

auth = CognitoAuth()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'success': False, 'error': 'Token missing'}), 401

        if token.startswith('Bearer '):
            token = token[7:]

        user = auth.get_user_from_token(token)

        if not user:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        # Add user to request context
        request.user = user

        return f(*args, **kwargs)

    return decorated


def provider_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # This would check if the user has provider role
        # Simplified for now
        return f(*args, **kwargs)

    return decorated