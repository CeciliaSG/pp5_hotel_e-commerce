# Generated by Django 4.2.13 on 2024-08-29 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0022_alter_servicecategory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslotavailability',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]