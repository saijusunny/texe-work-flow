# Generated by Django 4.0.2 on 2024-01-09 06:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texeclientapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='joindate',
            field=models.DateField(default=datetime.date(2024, 1, 9), null=True),
        ),
    ]
