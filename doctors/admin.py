from django.contrib import admin
from .models import Doctor, DoctorAppointments, DoctorNotification, DoctorSettings, BloodInventory

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'specialty']
   

@admin.register(DoctorAppointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'donor', 'patient', 'date', 'time']

    
@admin.register(DoctorNotification)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_read', 'created']
    list_filter = ['is_read']

@admin.register(DoctorSettings)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['doctor','email_notifications', 'sms_notifications', 'push_notifications']

@admin.register(BloodInventory)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['blood_group', 'quantity_ml', 'expiry_date']
    list_filter = ['blood_group']
