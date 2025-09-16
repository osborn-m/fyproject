# google_drive_utils.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Your folder ID
FOLDER_ID = "1a05iQE-PWyzFrVHtyV6yETjwf-jhiMVd"

# Path to your service account JSON key
SERVICE_ACCOUNT_FILE = "resources/credentials/service_account.json"

# Scopes for Google Drive API
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Initialize credentials and Drive service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

# Function to list files in folder
def list_files_in_folder():
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents",
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])

    files_data = []
    for file in items:
        file_id = file['id']
        files_data.append({
            "name": file['name'],
            "download_link": f"https://drive.google.com/uc?id={file_id}&export=download",
            "web_view_link": f"https://drive.google.com/file/d/{file_id}/view"
        })
    return files_data
