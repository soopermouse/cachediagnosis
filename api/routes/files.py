# cachemed/api/routes/files.py
from flask import request, jsonify
from .. import api_bp
from storage.uploader import FileUploader

uploader = FileUploader()

@api_bp.route('/files/upload', methods=['POST'])
def initiate_upload():
    """Get presigned URL for file upload"""
    try:
        data = request.json
        result = uploader.initiate_upload(data)
        return jsonify({'success': True, 'upload': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/files/<file_id>', methods=['GET'])
def get_file(file_id):
    """Get file metadata"""
    try:
        file_record = uploader.get_metadata(file_id)
        if not file_record:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return jsonify({'success': True, 'file': file_record})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/files/patient/<patient_id>', methods=['GET'])
def list_patient_files(patient_id):
    """List files for a patient"""
    try:
        files = uploader.list_for_patient(patient_id)
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500