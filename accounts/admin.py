from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('SheSkills', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SheSkills', {'fields': ('role', 'phone', 'email')}),
    )
