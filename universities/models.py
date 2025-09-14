from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # Public or Private
    founded = models.IntegerField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    # Contact Information
    contact_address = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_website = models.URLField(blank=True, null=True)

    # Rankings
    national_rank = models.IntegerField(blank=True, null=True)

    # Statistics
    total_students = models.IntegerField(blank=True, null=True)
    student_to_faculty_ratio = models.CharField(max_length=20, blank=True, null=True)

    # Admissions
    application_deadline = models.DateField(blank=True, null=True)

    # Tuition Fees
    domestic_undergraduate_min = models.IntegerField(blank=True, null=True)
    domestic_undergraduate_max = models.IntegerField(blank=True, null=True)
    domestic_currency = models.CharField(max_length=10, default="GHS")
    international_undergraduate_min = models.IntegerField(blank=True, null=True)
    international_undergraduate_max = models.IntegerField(blank=True, null=True)
    international_currency = models.CharField(max_length=10, default="USD")
    accommodation_min = models.IntegerField(blank=True, null=True)
    accommodation_max = models.IntegerField(blank=True, null=True)
    accommodation_currency = models.CharField(max_length=10, default="GHS")

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)
    universities = models.ManyToManyField(University, related_name='facilities')

    def __str__(self):
        return self.name


class Program(models.Model):
    university = models.ForeignKey(University, related_name="programs", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cutoff_points = models.CharField(max_length=50, default="15")
    requirements = models.CharField(max_length=255, default="Standard requirements")

    def __str__(self):
        return f"{self.name} - {self.university.name}"
