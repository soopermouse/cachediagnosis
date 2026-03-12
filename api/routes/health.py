# cachemed/api/routes/health.py
from flask import jsonify
from .. import api_bp
from datetime import datetime

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })