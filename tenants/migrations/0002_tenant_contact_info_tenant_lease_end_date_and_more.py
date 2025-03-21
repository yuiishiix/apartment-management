# Generated by Django 5.1.6 on 2025-03-21 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='contact_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='lease_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='lease_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
