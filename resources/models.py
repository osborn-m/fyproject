from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('Past Questions', 'Past Questions'),
        ('Lecture Notes', 'Lecture Notes'),
        ('Assignments', 'Assignments'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
