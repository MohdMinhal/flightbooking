# Generated by Django 5.0.1 on 2024-08-28 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0003_populate_origin_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('expired', 'Expired')], default='pending', max_length=20),
        ),
    ]