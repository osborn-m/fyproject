import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

# Try to load credentials from environment variable
service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

if service_account_json:
    # Parse JSON string from env var
    credentials_info = json.loads(service_account_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )
else:
    # Fallback to local service account file
    SERVICE_ACCOUNT_FILE = os.path.join(
        settings.BASE_DIR, "resources/utils/credentials/service_account.json"
    )
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

# Build Drive service
drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(file_path, file_name, folder_id=None):
    """
    Upload a file to Google Drive.
    Returns: (webViewLink, webContentLink)
    """
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink, webContentLink"
    ).execute()

    return file.get("webViewLink"), file.get("webContentLink")
