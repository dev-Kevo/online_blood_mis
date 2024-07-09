from django.contrib import admin
from patients.models import Patient, PatientAppointment, PatientDonations


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'medical_record_number']
    # search_fields = ['user__username', 'medical_record_c_number', 'blood_type']


@admin.register(PatientAppointment)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'time', 'location']
    
@admin.register(PatientDonations)
class PatientDonationsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount_of_blood_used']

