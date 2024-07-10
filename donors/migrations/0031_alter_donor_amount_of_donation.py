# Generated by Django 5.0.6 on 2024-07-10 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0030_alter_donor_blood_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='amount_of_donation',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='How much Money paid for the donation', max_digits=10, null=True),
        ),
    ]
