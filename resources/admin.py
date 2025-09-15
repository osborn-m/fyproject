from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'uploaded_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)
