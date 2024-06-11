from django.contrib import admin
from patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'medical_record_number']
    # search_fields = ['user__username', 'medical_record_c_number', 'blood_type']


