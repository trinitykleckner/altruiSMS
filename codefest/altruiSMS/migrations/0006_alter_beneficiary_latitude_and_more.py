# Generated by Django 4.0.3 on 2022-04-07 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altruiSMS', '0005_delete_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='latitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='longitude',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]