from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
from donors.models import Donor, DonorSettings
from patients.models import Patient
import uuid

@receiver(post_save, sender=CustomUser)
def update_user_signal(sender, instance, created, **kwargs):
    if created and instance.is_donor:
        instance.is_verified = False
        instance.save(update_fields=['is_verified'])  # Save to persist the changes

        # create a donor profile
        donor = Donor.objects.create(user=instance)
        donor.medical_record_number = f"MR-{str(uuid.uuid4())[:8].upper()}"
        donor.save()

        # create a donor settings profile
        donor_settings = DonorSettings.objects.create(donor=instance)
        donor_settings.save()


    elif created and instance.is_patient:
        patient = Patient.objects.create(user=instance)
        patient.medical_record_number = f"MR-{str(uuid.uuid4())[:8].upper()}"
        patient.save()

    elif created and instance.is_doctor:
        pass

    
     


