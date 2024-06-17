from django.db import models
from django.conf import settings
from donors.models import Donor
from patients.models import Patient


class Preffered_Contact_Method(models.TextChoices):
    EMAIL = 'email', 'Email'
    PHONENUMBER = 'phonenumber', 'Phonenumber'

class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    ATTENTED = 'COMPLETED', 'COMPLETED'
    CANCLED = 'CANCLED', 'CANCLED'

class AppointmentsFromChoices(models.TextChoices):
    DONOR = 'DONOR', 'DONOR'
    PATIENT = 'PATIENT', 'PATIENT'
    

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
    is_available = models.BooleanField(default=True)
    no_appointments = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    @property
    def get_availability_status(self):
        return self.is_available
    
    def update_no_appointments(self, state):
        """
        Update the number of appointments baseed on the state.
        states:
            - add (basically adding 1 to the appointments)
            - substract (substracting 1 to the appointments)
        """
        if state == 'add':
            self.no_appointments += 1
            print(f'Successfully added 1 to {self.user}"s Apointments ')
        else:
            self.no_appointments -= 1
            print(f'Successfully REMOVED 1 from {self.user}"s Apointments ')
    
    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialty})"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class DoctorAppointments(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=AppointmentStatus, default=AppointmentStatus.PENDING)
    note = models.CharField(max_length=250, default='Always make sure to leave a comment')
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

class DoctorNotification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    notify_from = models.CharField(max_length=200,null=True, blank=True)
    message = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)
    modified = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Notification: {self.message}'
    

class DoctorSettings(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    default_notification_method = models.CharField(max_length=255, default=Preffered_Contact_Method.EMAIL, choices=Preffered_Contact_Method)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.doctor.user.username} Settings'

    class Meta:
        verbose_name = "Doctor Settings"
        verbose_name_plural = "Doctor Settings"

