# Generated by Django 5.0.6 on 2024-06-13 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0017_alter_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='number_of_donations',
            field=models.PositiveIntegerField(blank=True, max_length=12, null=True),
        ),
    ]