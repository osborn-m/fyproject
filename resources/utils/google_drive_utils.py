# resources/utils/google_drive_utils.py

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Drive folder ID
FOLDER_ID = "1a05iQE-PWyzFrVHtyV6yETjwf-jhiMVd"

# Google Drive API scopes
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Attempt to load credentials from environment variable
service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

if service_account_json:
    try:
        SERVICE_ACCOUNT_INFO = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, scopes=SCOPES
        )
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON in GOOGLE_SERVICE_ACCOUNT_JSON") from e
else:
    # Fallback to local service account JSON file
    SERVICE_ACCOUNT_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "credentials",
        "service_account.json"
    )
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Service account file not found: {SERVICE_ACCOUNT_FILE}")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

# Initialize Google Drive service
drive_service = build("drive", "v3", credentials=credentials)

def list_files_in_folder():
    """
    List all files in the specified Google Drive folder.
    Returns a list of dictionaries with:
        - name: file name
        - download_link: direct download link
        - web_view_link: link to view in browser
    """
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute()

    items = results.get("files", [])

    files_data = []
    for file in items:
        file_id = file["id"]
        files_data.append({
            "name": file["name"],
            "download_link": f"https://drive.google.com/uc?id={file_id}&export=download",
            "web_view_link": f"https://drive.google.com/file/d/{file_id}/view"
        })

    return files_data
