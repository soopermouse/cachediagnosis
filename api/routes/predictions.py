# cachemed/api/routes/predictions.py
from flask import request, jsonify
from .. import api_bp
from core.services.prediction_service import PredictionService

prediction_service = PredictionService()

@api_bp.route('/predict/<patient_id>', methods=['POST'])
def predict(patient_id):
    """Generate prediction for a patient"""
    try:
        prediction = prediction_service.generate(patient_id)
        return jsonify({'success': True, 'prediction': prediction})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/predictions/<patient_id>', methods=['GET'])
def get_predictions(patient_id):
    """Get prediction history for a patient"""
    try:
        predictions = prediction_service.get_history(patient_id)
        return jsonify({'success': True, 'predictions': predictions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500