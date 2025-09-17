import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load service account JSON from environment variable
SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

if not SERVICE_ACCOUNT_JSON:
    raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set.")

SCOPES = ["https://www.googleapis.com/auth/drive"]

# Parse JSON string into a dict
service_account_info = json.loads(SERVICE_ACCOUNT_JSON)

credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(file_path, file_name, folder_id=None):
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink, webContentLink"
    ).execute()

    return file.get("webViewLink"), file.get("webContentLink")
