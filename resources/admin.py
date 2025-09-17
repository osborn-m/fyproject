from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
