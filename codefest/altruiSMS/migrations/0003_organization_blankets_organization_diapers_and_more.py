# Generated by Django 4.0.3 on 2022-04-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altruiSMS', '0002_location_organization_remove_beneficiary_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='blankets',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='diapers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='food',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='sanitary',
            field=models.BooleanField(default=False),
        ),
    ]
