# Generated by Django 5.0.6 on 2024-07-08 20:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0025_alter_donorsettings_default_notification_method_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Donations',
            new_name='DonorDonations',
        ),
    ]
