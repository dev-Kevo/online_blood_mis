from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
from donors.models import Donor

@receiver(post_save, sender=CustomUser)
def update_user_signal(sender, created, instance, *args, **kwargs):
    if created:
        instance.is_verified = False
        print(instance.is_donor)


# @receiver(post_save, sender=CustomUser)        
# def create_donor(sender, created, instance, *args, **kwargs):
#     if created:
#         print("The created donor is: ", instance)
#         print(sender.is_donor)

#         if instance.is_donor:
#             print("The created donore is: ", instance) 
#             Donor(user=instance).save()



