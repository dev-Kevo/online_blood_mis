from django.contrib import admin

from .models import Donor

# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'donation_location',
        'date_of_donation',
    ]


