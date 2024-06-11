# Generated by Django 5.0.6 on 2024-06-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0007_donor_medical_record_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3),
        ),
    ]