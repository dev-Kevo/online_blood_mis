# Generated by Django 5.0.6 on 2024-06-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0014_rename_benefiaciary_appointment_beneficiary'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], default='PENDING', max_length=20),
        ),
    ]
