# Generated by Django 5.1.6 on 2025-03-21 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('facility', 'date', 'start_time')},
        ),
    ]
