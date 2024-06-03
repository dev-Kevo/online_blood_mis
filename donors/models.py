from django.db import models
from core.models import CustomeUser

# Create your models here.
class Donor(models.Model):

    class GenderSelect(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class Preffered_Contact_Method(models.TextChoices):
        EMAIL = 'email', 'Email'
        PHONENUMBER = 'phonenumber', 'Phonenumber'

    class Preffered_Contact_Method(models.TextChoices):
        ONE_TIME = 'One-time donations'
        RECURRING = 'Recurring donations'
        PLANNED = 'Planned donations'
        TRI_MEM = 'Tribute or memorial donations'
        STOCK = 'Stock donations'
        KIND = 'In-kind donations'
        MATCHING = 'Matching donations'
        WORKPLACE = 'Workplace donations'
        EVENT = 'Event donations'
    donor = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
    preferred_contact_method = models.CharField(blank=True, max_length=255)
    total_number_of_donations = models.IntegerField(blank=True)
    is_eligible_to_donate = models.BooleanField(default=True, blank=True)
    type_donation = models.CharField(max_length=200, blank=True)
    profile_photo = models.ImageField(upload_to='donors', default='', blank=True)
    address = models.TextField(blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username
    


class PrefferedDonationLocations(models.TextChoices):
    NAIROBI = 'Nairobi Blood Transfusion Centre', 'Nairobi Blood Transfusion Centre'
    MOMBASA = 'Mombasa Blood Transfusion Centre', 'Mombasa Blood Transfusion Centre'
    KISUMU = 'Kisumu Blood Transfusion Centre', 'Kisumu Blood Transfusion Centre'
    EMBU = 'Embu Blood Transfusion Centre', 'Embu Blood Transfusion Centre'
    NAKURU = 'Nakuru Blood Transfusion Centre', 'Nakuru Blood Transfusion Centre'
    ELDORET = 'Eldoret Blood Transfusion Centr', 'Eldoret Blood Transfusion Centr'


class Record(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    preffered_donation_location = models.CharField(max_length=90, choices=PrefferedDonationLocations.choices)

    def __str__(self) -> str:
        return self.donor.username
    
