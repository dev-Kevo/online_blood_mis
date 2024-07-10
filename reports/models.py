from django.db import models
from django.conf import settings

class ReportType(models.TextChoices):
    TOTAL_DONATIONS = 'Donations', 'Donation Report'
    APPOINTMENTS = 'Appointments', 'Appointments  Report'
    BLOOD_INVENTORY = 'Blood Inventory', 'Blood Inventory Report'
    DONORS = 'Donors', 'Donors Report'
    PATIENTS = 'Patients', 'Patients Report'
    DOCTORS = 'Doctors', 'Doctors Report'
    FINANCIAL = 'Financial', 'Financial Report'


class Report(models.Model):
    report_type = models.CharField(max_length=50, choices=ReportType.choices)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = '-created',
        verbose_name = "Report"
        verbose_name_plural = "Reports"


    def __str__(self):
        return f"{self.report_type} Report"
    
