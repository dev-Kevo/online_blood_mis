from django.contrib import admin

from .models import Donor, Record

# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'donor', 'is_eligible_to_donate'
    ]

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [
        'donor', 'preffered_donation_location'
    ]
