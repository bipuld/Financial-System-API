# Generated by Django 5.1.3 on 2024-11-29 08:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date_received',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]