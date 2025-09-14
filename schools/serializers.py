from rest_framework import serializers
from .models import Facility, Program, Course, School, SchoolCourse

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "program"]

class ProgramSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = Program
        fields = ["id", "name", "courses"]

        

class SchoolCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = SchoolCourse
        fields = ["id", "name", "course", "source_program", "is_custom", "is_active"]

class SchoolSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)
    school_courses = SchoolCourseSerializer(many=True, read_only=True)

    facility_ids = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all(), many=True, write_only=True, required=False)
    program_ids = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = School
        fields = [
            "id","name","region","district","passed","residency","gender","description","wassce_ranking",
            "address","phone","email","website",
            "facilities","programs","school_courses","facility_ids","program_ids"
        ]

    def create(self, validated_data):
        facility_ids = validated_data.pop("facility_ids", [])
        program_ids = validated_data.pop("program_ids", [])
        school = super().create(validated_data)
        if facility_ids:
            school.facilities.set(facility_ids)
        if program_ids:
            school.programs.set(program_ids)
        return school

    def update(self, instance, validated_data):
        facility_ids = validated_data.pop("facility_ids", None)
        program_ids = validated_data.pop("program_ids", None)
        school = super().update(instance, validated_data)
        if facility_ids is not None:
            school.facilities.set(facility_ids)
        if program_ids is not None:
            school.programs.set(program_ids)
        return school
