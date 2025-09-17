import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

# Path to your service account JSON
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'resources/utils/credentials/service_account.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(file_path, file_name, folder_id=None):
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = None
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(file_path, resumable=True)
    
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink, webContentLink'
    ).execute()
    
    return file.get('webViewLink'), file.get('webContentLink')
