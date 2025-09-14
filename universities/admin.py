from django.contrib import admin
from .models import University, Program, Facility

class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1

class FacilityInline(admin.TabularInline):
    model = Facility.universities.through
    extra = 1

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'founded', 'national_rank')
    inlines = [ProgramInline, FacilityInline]

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'cutoff_points', 'requirements')

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
