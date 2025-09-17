from rest_framework import generics
from .models import Resource
from .serializers import ResourceSerializer
from .utils.google_drive_utils import upload_file_to_drive
import os
from django.conf import settings

class ResourceListView(generics.ListAPIView):
    queryset = Resource.objects.all().order_by('-uploaded_at')
    serializer_class = ResourceSerializer
