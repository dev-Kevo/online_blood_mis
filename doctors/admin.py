from django.contrib import admin

from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'specialty']
    # search_fields = ['user__username', 'license_number', 'specialty']