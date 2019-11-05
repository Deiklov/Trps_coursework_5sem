# Generated by Django 2.2 on 2019-10-31 22:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askpupkin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='data_create',
            field=models.DateField(default=datetime.date(2019, 11, 1)),
        ),
        migrations.AlterField(
            model_name='answer',
            name='data_create',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
