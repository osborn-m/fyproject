# resources/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.google_drive_utils import list_files_in_folder

@api_view(['GET'])
def google_drive_resources(request):
    """
    Returns a list of files in the specified Google Drive folder.
    Each file contains: name, mimeType, webViewLink, and downloadLink.
    """
    try:
        files = list_files_in_folder()
        return Response({'success': True, 'files': files})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)
