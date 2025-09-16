# resources/urls.py

from django.urls import path
from .views import google_drive_resources

urlpatterns = [
    path('', google_drive_resources, name='google_drive_resources'),
]
