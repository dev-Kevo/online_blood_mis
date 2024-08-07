# Generated by Django 5.0.6 on 2024-07-08 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_patientdonations_delete_donations'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='amount_of_blood_used',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='follow_up_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='treatment_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
