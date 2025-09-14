from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model that adds a user_type field.
    """
    USER_TYPES = [
        ('JHS', 'Junior High School'),
        ('SHS', 'Senior High School'),
        ('UNI', 'University'),
        ('OTH', 'Other'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='OTH')

    def __str__(self):
        return self.username
