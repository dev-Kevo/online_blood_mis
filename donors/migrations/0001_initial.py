# Generated by Django 5.0.6 on 2024-05-24 11:46

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
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_contact_method', models.CharField(blank=True, max_length=255)),
                ('total_number_of_donations', models.IntegerField(blank=True)),
                ('is_eligible_to_donate', models.BooleanField(blank=True, default=True)),
                ('type_donation', models.CharField(blank=True, max_length=200)),
                ('profile_photo', models.ImageField(blank=True, default='', upload_to='donors')),
                ('address', models.TextField(blank=True)),
                ('weight_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('last_donation_date', models.DateField(blank=True, null=True)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preffered_donation_location', models.CharField(choices=[('Nairobi Blood Transfusion Centre', 'Nairobi Blood Transfusion Centre'), ('Mombasa Blood Transfusion Centre', 'Mombasa Blood Transfusion Centre'), ('Kisumu Blood Transfusion Centre', 'Kisumu Blood Transfusion Centre'), ('Embu Blood Transfusion Centre', 'Embu Blood Transfusion Centre'), ('Nakuru Blood Transfusion Centre', 'Nakuru Blood Transfusion Centre'), ('Eldoret Blood Transfusion Centr', 'Eldoret Blood Transfusion Centr')], max_length=90)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donors.donor')),
            ],
        ),
    ]
