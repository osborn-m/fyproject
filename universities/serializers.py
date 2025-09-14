from rest_framework import serializers
from .models import University, Facility, Program

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

# class UniversitySerializer(serializers.ModelSerializer):
#     facilities = FacilitySerializer(many=True, read_only=True)
#     programs = ProgramSerializer(many=True, read_only=True)

#     class Meta:
#         model = University
#         fields = [
#             'id', 'name', 'type', 'founded', 'location', 'description',
#             'contact_address', 'contact_phone', 'contact_email', 'contact_website',
#             'national_rank', 'total_students', 'student_to_faculty_ratio',
#             'application_deadline', 'domestic_undergraduate_min', 'domestic_undergraduate_max',
#             'domestic_undergraduate_currency', 'international_undergraduate_min',
#             'international_undergraduate_max', 'international_undergraduate_currency',
#             'accommodation_min', 'accommodation_max', 'accommodation_currency',
#             'facilities', 'programs'
#         ]



class UniversitySerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = [
            'id', 'name', 'type', 'founded', 'location', 'description',
            'contact_address', 'contact_phone', 'contact_email', 'contact_website',
            'national_rank', 'total_students', 'student_to_faculty_ratio',
            'application_deadline', 'domestic_undergraduate_min', 'domestic_undergraduate_max',
            'domestic_currency',  # <- fixed
            'international_undergraduate_min', 'international_undergraduate_max',
            'international_currency',  # <- fixed
            'accommodation_min', 'accommodation_max', 'accommodation_currency',
            'facilities', 'programs'
        ]
