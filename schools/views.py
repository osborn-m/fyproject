from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import School, Program, Facility, Course, SchoolCourse
from .serializers import SchoolSerializer, ProgramSerializer, FacilitySerializer, CourseSerializer, SchoolCourseSerializer


from rest_framework import viewsets
from .models import School
from .serializers import SchoolSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all().prefetch_related(
        "programs",
        "facilities",
    )
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]  

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.prefetch_related("courses")
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]  

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [AllowAny]  

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  

class SchoolCourseViewSet(viewsets.ModelViewSet):
    queryset = SchoolCourse.objects.all()
    serializer_class = SchoolCourseSerializer
    permission_classes = [AllowAny]  
