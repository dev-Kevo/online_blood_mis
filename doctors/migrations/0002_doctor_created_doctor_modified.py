# Generated by Django 5.0.6 on 2024-06-06 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='created',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='modified',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
