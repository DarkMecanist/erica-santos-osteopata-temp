# Generated by Django 3.1.7 on 2021-07-18 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eso', '0002_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 18, 12, 58, 15, 628486)),
            preserve_default=False,
        ),
    ]
