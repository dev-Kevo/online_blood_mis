# Generated by Django 5.0.6 on 2024-07-10 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0013_alter_patient_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=12, null=True),
        ),
    ]
