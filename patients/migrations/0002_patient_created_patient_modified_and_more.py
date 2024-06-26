# Generated by Django 5.0.6 on 2024-06-06 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='created',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='modified',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='blood_type',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='medical_record_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
