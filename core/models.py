from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)




# class BloodGroup(models.TextChoices):
#     'A PLUS',
# 
BloodGroup = (
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B-'),
    ('O+','O+'),
    ('O-','O-'),
    ('AB+','AB+'),
    ('AB-','AB-'),
) 

class CustomUser(AbstractUser):
    id_number = models.CharField(max_length=8, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    next_of_kin = models.CharField(max_length=255, blank=True)
    next_of_kin_phone_number = models.CharField(max_length=12, blank=True)
    blood_group = models.CharField(max_length=10, choices=BloodGroup, blank=True) # some action to take place in here
    is_doctor = models.BooleanField(null=True)
    is_patient = models.BooleanField(null=True)
    is_donor = models.BooleanField(null=True)
    is_verified = models.BooleanField(null=True)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)


    objects = CustomUserManager()

    def __str__(self) -> str:
        return str(self.username)