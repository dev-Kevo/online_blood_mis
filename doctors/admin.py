from django.contrib import admin
from .models import Doctor, DoctorAppointments, DoctorNotification

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'specialty']
   

@admin.register(DoctorAppointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'donor', 'patient', 'date', 'time']

    
@admin.register(DoctorNotification)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_read', 'created']
    