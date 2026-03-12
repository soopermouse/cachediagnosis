# cachemed/storage/uploader.py
import uuid
from .s3_client import S3Client
from database.repositories.file_repo import FileRepository


class FileUploader:
    def __init__(self):
        self.s3 = S3Client()
        self.repo = FileRepository()

    def initiate_upload(self, data):
        """Start file upload process"""
        file_id = str(uuid.uuid4())
        key = f"patients/{data['patientId']}/{file_id}-{data['filename']}"

        # Generate upload URL
        upload_url = self.s3.generate_upload_url(
            key=key,
            content_type=data['mimeType']
        )

        # Create file record
        file_record = self.repo.create({
            'fileId': file_id,
            'patientId': data['patientId'],
            'filename': data['filename'],
            'mimeType': data['mimeType'],
            'fileType': data.get('fileType', 'unknown'),
            'storagePath': key
        })

        return {
            'fileId': file_id,
            'uploadUrl': upload_url,
            'expiresIn': 3600,
            'fileRecord': file_record
        }

    def get_metadata(self, file_id):
        """Get file metadata"""
        return self.repo.get(file_id)

    def list_for_patient(self, patient_id):
        """List files for patient"""
        return self.repo.list_for_patient(patient_id)

    def confirm_upload(self, file_id):
        """Confirm upload completed"""
        return self.repo.update_status(file_id, 'uploaded')