from django.db import models
from django.conf import  settings



class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    ATTENTED = 'COMPLETED', 'COMPLETED'
    CANCLED = 'CANCLED', 'CANCLED'

class PrefferedDonationLocations(models.TextChoices):
    NAIROBI = 'Nairobi Blood Transfusion Centre', 'Nairobi Blood Transfusion Centre'
    MOMBASA = 'Mombasa Blood Transfusion Centre', 'Mombasa Blood Transfusion Centre'
    KISUMU = 'Kisumu Blood Transfusion Centre', 'Kisumu Blood Transfusion Centre'
    EMBU = 'Embu Blood Transfusion Centre', 'Embu Blood Transfusion Centre'
    NAKURU = 'Nakuru Blood Transfusion Centre', 'Nakuru Blood Transfusion Centre'
    ELDORET = 'Eldoret Blood Transfusion Centr', 'Eldoret Blood Transfusion Centr'

class Patient(models.Model):

    class BloodGroup(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-',
        UNKNOWN = 'UNKNOWN', 'UNKNOWN'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    profile_photo = models.ImageField(upload_to='donors', default='no_pic.jpg', blank=True)
    id_number = models.CharField(max_length=12, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    medical_record_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BloodGroup, blank=True, default=BloodGroup.UNKNOWN)
    medical_conditions = models.TextField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    update_last_blood_charge_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = '-created',

    def update_last_blood_charge_date(self, date):
        self.update_last_blood_charge_date = date

    @property
    def get_profile_pic(self):
        return self.profile_photo.url

    def __str__(self):
        return f"{self.user.username}"   

class PatientAppointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointment')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255, choices=PrefferedDonationLocations)
    status = models.CharField(max_length=20, choices=AppointmentStatus, default=AppointmentStatus.PENDING)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = '-created',

    def __str__(self):
        return f"Appointment for {self.patient} on {self.date} at {self.time}"
    
class PatientDonations(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_donations')
    amount_of_blood_used = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Amount of blood donated in ml")
    treatment_notes = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = '-created',
        verbose_name = "Patient Recharge"
        verbose_name_plural = "Patient Recharges"

    def __str__(self):
        return f"Blood Recharge by {self.patient} on {self.created}"  
