# Generated by Django 5.0.6 on 2024-06-13 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0012_remove_donor_date_of_donation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='description',
            new_name='benefiaciary',
        ),
    ]
