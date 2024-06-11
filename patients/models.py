from django.db import models
from django.conf import  settings


class Patient(models.Model):

    class BloodGroup(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'




    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    profile_photo = models.ImageField(upload_to='donors', default='no_pic.jpg', blank=True)
    id_number = models.CharField(max_length=12, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    medical_record_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BloodGroup, blank=True)
    medical_conditions = models.TextField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    @property
    def get_profile_pic(self):
        return self.profile_photo

    def __str__(self):
        return f"{self.user.username}"
    
   
