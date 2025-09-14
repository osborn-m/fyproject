from django.contrib import admin
from .models import Scholarship

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('scholarship_name', 'level', 'category', 'application_deadline')
    search_fields = ('scholarship_name',)
    list_filter = ('level', 'category')
