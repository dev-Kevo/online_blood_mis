# Generated by Django 5.0.6 on 2024-06-14 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_doctornotification_notify_from'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Appointments',
            new_name='DoctorAppointments',
        ),
    ]
