# Generated by Django 5.0.6 on 2024-07-10 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0019_doctor_number_max_appointments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital_affiliated',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='no_appointments',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(blank=True, choices=[('Hematology', 'Hematology'), ('Transfusion Medicine', 'Transfusion Medicine'), ('Internal Medicine', 'Internal Medicine'), ('Emergency Medicine', 'Emergency Medicine'), ('Anesthesiology', 'Anesthesiology'), ('General Surgery', 'General Surgery')], max_length=100, null=True),
        ),
    ]
