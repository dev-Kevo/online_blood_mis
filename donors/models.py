from django.db import models
from django.db.models import Sum
from core.models import CustomUser
from django.conf import settings



class GenderSelect(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

class Preffered_Contact_Method(models.TextChoices):
    EMAIL = 'email', 'Email'
    PHONENUMBER = 'phonenumber', 'Phonenumber'

class DonationType(models.TextChoices):
    ONE_TIME = 'One-time donations'
    RECURRING = 'Recurring donations'
    PLANNED = 'Planned donations'
    TRI_MEM = 'Tribute or memorial donations'
    STOCK = 'Stock donations'
    KIND = 'In-kind donations'
    MATCHING = 'Matching donations'
    WORKPLACE = 'Workplace donations'
    EVENT = 'Event donations'

class PrefferedDonationLocations(models.TextChoices):
    NAIROBI = 'Nairobi Blood Transfusion Centre', 'Nairobi Blood Transfusion Centre'
    MOMBASA = 'Mombasa Blood Transfusion Centre', 'Mombasa Blood Transfusion Centre'
    KISUMU = 'Kisumu Blood Transfusion Centre', 'Kisumu Blood Transfusion Centre'
    EMBU = 'Embu Blood Transfusion Centre', 'Embu Blood Transfusion Centre'
    NAKURU = 'Nakuru Blood Transfusion Centre', 'Nakuru Blood Transfusion Centre'
    ELDORET = 'Eldoret Blood Transfusion Centr', 'Eldoret Blood Transfusion Centr'

class BloodGroup(models.TextChoices):
    A_POS = 'A+', 'A+'
    A_NEG = 'A-', 'A-'
    B_POS = 'B+', 'B+'
    B_NEG = 'B-', 'B-'
    AB_POS = 'AB+', 'AB+'
    AB_NEG = 'AB-', 'AB-'
    O_POS = 'O+', 'O+'
    O_NEG = 'O-', 'O-'
    UNKNOWN = 'UNKNOWN', 'UNKNOWN'

class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    COMPLETED = 'COMPLETED', 'COMPLETED'
    CANCLED = 'CANCLED', 'CANCLED'

class Donor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medical_record_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='donors', default='no_pic.jpg', blank=True)
    id_number = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=12, choices=GenderSelect, null=True, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=12,help_text='If you are not sure, leave it as it is. The doctor will update it for you.', choices=BloodGroup, default=BloodGroup.UNKNOWN)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    donation_location = models.CharField(max_length=255, choices=PrefferedDonationLocations, null=True, blank=True)
    preferred_contact_method = models.CharField(blank=True, max_length=255, choices=Preffered_Contact_Method, null=True)
        

    # these fields will be populated when the user vistis the station
    is_eligible_to_donate = models.BooleanField(default=True, blank=True) #----> doctor to conduct a survey
    type_donation = models.CharField(max_length=200, blank=True, choices=DonationType)
    amount_of_donation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    number_of_donations = models.PositiveIntegerField(null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)

    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    
    def update_last_donation_date(self, date):
        self.last_donation_date = date
    
    @property
    def get_profile_pic(self):
        return self.profile_photo.url
    
    
    def update_no_of_donations(self):
       self.number_of_donations += 1
    
    @property
    def get_no_of_donations(self):
        return self.number_of_donations
    
    @classmethod
    def get_total_donations(cls):
        return cls.objects.aggregate(total_donations=Sum('number_of_donations'))['total_donations'] or 0

    def __str__(self) -> str:
        return self.user.username
    

class Donations(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    beneficiary = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):

        return f"Donation by {self.donor} on {self.created}"
    

class DonorAppointment(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_appointment')
    date = models.DateField()
    time = models.TimeField()
    beneficiary = models.TextField()
    location = models.CharField(max_length=255, choices=PrefferedDonationLocations)
    status = models.CharField(max_length=20, choices=AppointmentStatus, default=AppointmentStatus.PENDING)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = '-created',

    def __str__(self):
        return f"Appointment for {self.donor} on {self.date} at {self.time}"
    

class Notification(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.donor} - {self.message[:20]}"
    

class Impact(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    people_helped = models.IntegerField()
    projects_supported = models.IntegerField()
    date_updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now=True, null=True, blank=True)
    modified = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Impact for {self.donor}"

    


    
