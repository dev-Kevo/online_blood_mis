from django.db import models
from django.conf import settings

class Doctor(models.Model):

    SPECIALTY_CHOICES = [
        ('Hematology', 'Hematology'),
        ('Transfusion Medicine', 'Transfusion Medicine'),
        ('Internal Medicine', 'Internal Medicine'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('Anesthesiology', 'Anesthesiology'),
        ('General Surgery', 'General Surgery'),
        # Add more specialties as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    hospital_affiliated = models.CharField(max_length=100)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} ({self.specialty})"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
