# Generated by Django 5.0.6 on 2024-06-17 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0014_alter_doctorappointments_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications', models.BooleanField(default=True)),
                ('sms_notifications', models.BooleanField(default=True)),
                ('push_notifications', models.BooleanField(default=True)),
                ('default_notification_method', models.CharField(choices=[('email', 'Email'), ('phonenumber', 'Phonenumber')], default='email', max_length=255)),
                ('created', models.DateField(auto_now=True, null=True)),
                ('modified', models.DateField(auto_now_add=True, null=True)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
            ],
            options={
                'verbose_name': 'Doctor Settings',
                'verbose_name_plural': 'Doctor Settings',
            },
        ),
    ]
