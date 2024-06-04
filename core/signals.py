from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser

@receiver(post_save, sender=CustomUser)
def update_user_signal(sender, created, instance, *args, **kwargs):
    if created:
        instance.is_verified = False
        
