from django.contrib import admin
from .models import Facility, Program, Course, School, SchoolCourse


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CourseInline(admin.TabularInline):
    model = Course
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [CourseInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "program")
    list_filter = ("program",)
    search_fields = ("name",)


class SchoolCourseInline(admin.TabularInline):
    model = SchoolCourse
    extra = 1


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "district", "wassce_ranking")
    list_filter = ("region", "district", "gender", "residency")
    search_fields = ("name", "region", "district")
    filter_horizontal = ("facilities", "programs")
    inlines = [SchoolCourseInline]


@admin.register(SchoolCourse)
class SchoolCourseAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "source_program", "is_custom", "is_active")
    list_filter = ("is_custom", "is_active", "source_program")
    search_fields = ("name", "school__name")
