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
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['donor','blood_group', 'quantity', 'expiry_date']
    list_filter = ['blood_group']
