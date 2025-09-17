from django import forms
from .models import Resource
from .utils.google_drive_utils import upload_file_to_drive
import os
from django.conf import settings

class ResourceAdminForm(forms.ModelForm):
    # Override file field to accept uploads in admin
    file_upload = forms.FileField(required=True, label="Upload File")

    class Meta:
        model = Resource
        fields = ("name", "category", "file_upload")

    def save(self, commit=True):
        instance = super().save(commit=False)

        uploaded_file = self.cleaned_data.get("file_upload")
        if uploaded_file:
            # Save temporarily to media folder
            temp_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(temp_path, "wb+") as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # Upload to Google Drive
            drive_file = upload_file_to_drive(temp_path, uploaded_file.name)

            # Remove temp file
            os.remove(temp_path)

            # Update instance fields with Google Drive links
            instance.file = drive_file["download_link"]
            instance.view_link = drive_file["view_link"]

        if commit:
            instance.save()
        return instance
