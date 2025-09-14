from django.db import models
from django.db.models import Q, UniqueConstraint

class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Program(models.Model):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.name

class Course(models.Model):
    program = models.ForeignKey(Program, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    class Meta:
        unique_together = ("program", "name")
    def __str__(self): return f"{self.name} ({self.program.name})"

class School(models.Model):
    RESIDENCY_CHOICES = [("Day", "Day"), ("Boarding", "Boarding")]
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Mixed", "Mixed")]

    # Overview
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    passed = models.IntegerField(default=0)
    residency = models.CharField(
    max_length=20,
    choices=RESIDENCY_CHOICES,
    default="boarding"
)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True)
    wassce_ranking = models.IntegerField(blank=True, null=True)

    # Contact
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=50, default="Contact the Ghana Education Service for details")
    email = models.CharField(max_length=255, default="Contact the school administration")
    website = models.CharField(max_length=255, default="Contact the school administration")

    facilities = models.ManyToManyField(Facility, blank=True)
    programs = models.ManyToManyField(Program, blank=True)
    courses = models.ManyToManyField(Course, through="SchoolCourse", blank=True)

    def __str__(self): return self.name

class SchoolCourse(models.Model):
    school = models.ForeignKey(School, related_name="school_courses", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="school_offerings", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    source_program = models.ForeignKey(Program, null=True, blank=True, on_delete=models.SET_NULL)
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["school", "course"], condition=Q(course__isnull=False), name="unique_school_course"),
            UniqueConstraint(fields=["school", "name"], name="unique_school_course_name"),
        ]
    def __str__(self): return f"{self.name} @ {self.school.name}"
