from django.db import models
from django.utils import timezone

class Scholarship(models.Model):
    # Choice fields
    CATEGORY_CHOICES = [
        ("Government", "Government"),
        ("Corporate", "Corporate"),
        ("NGO", "NGO"),
        ("Private/Foundation", "Private/Foundation"),
        ("University", "University"),
        ("Other", "Other"),
    ]

    LEVEL_CHOICES = [
        ("Undergraduate", "Undergraduate"),
        ("Postgraduate", "Postgraduate"),
        ("Vocational", "Vocational"),
        ("Undergraduate & Postgraduate", "Undergraduate & Postgraduate"),
        ("Other", "Other"),
    ]

    # Core fields
    scholarship_name = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    description = models.TextField()
    application_deadline = models.DateField(null=True, blank=True)
    eligibility_requirements = models.JSONField(default=list) 
    benefits = models.JSONField(default=list)                  
    application_process = models.JSONField(default=list)       
    website_or_contact = models.URLField(max_length=500, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    application_url = models.URLField(max_length=500, blank=True, null=True)
    

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.scholarship_name
