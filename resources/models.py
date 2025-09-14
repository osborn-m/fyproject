from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("Academic", "Academic"),
        ("Application", "Application"),
        ("Scholarship", "Scholarship"),
        ("Past Questions", "Past Questions"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to="resources/")  # Files stored in MEDIA_ROOT/resources/

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
