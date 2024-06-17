# Generated by Django 5.0.6 on 2024-06-17 08:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0024_donorsettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='donorsettings',
            name='default_notification_method',
            field=models.CharField(choices=[('email', 'Email'), ('phonenumber', 'Phonenumber')], default='email', max_length=255),
        ),
        migrations.AlterField(
            model_name='donorsettings',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor_settings', to=settings.AUTH_USER_MODEL),
        ),
    ]
