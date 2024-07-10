from django.contrib import admin

from .models import Donor, DonorDonations, DonorAppointment, Notification, Impact, DonorSettings

# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'donation_location',
    ]


@admin.register(DonorDonations)
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



@admin.register(DonorSettings)
class DonorSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'donor',
        'default_notification_method',
    ]