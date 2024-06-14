from django.contrib import admin

from .models import Donor, Donations, DonorAppointment, Notification, Impact

# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'donation_location',
    ]


@admin.register(Donations)
class DonationsAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'beneficiary',
        'amount',
        'created',
    ]

@admin.register(DonorAppointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'beneficiary',
        'date',
        'time',
    ]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'message',
        'is_read',
    ]

@admin.register(Impact)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'people_helped',
        'projects_supported',
    ]


