# Generated by Django 5.0.6 on 2024-06-06 20:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=20, unique=True)),
                ('specialty', models.CharField(choices=[('Hematology', 'Hematology'), ('Transfusion Medicine', 'Transfusion Medicine'), ('Internal Medicine', 'Internal Medicine'), ('Emergency Medicine', 'Emergency Medicine'), ('Anesthesiology', 'Anesthesiology'), ('General Surgery', 'General Surgery')], max_length=100)),
                ('hospital_affiliated', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
    ]