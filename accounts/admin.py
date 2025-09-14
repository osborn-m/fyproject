from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
