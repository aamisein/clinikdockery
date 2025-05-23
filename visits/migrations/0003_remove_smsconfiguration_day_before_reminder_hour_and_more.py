# Generated by Django 5.2.1 on 2025-05-09 15:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_smsconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsconfiguration',
            name='day_before_reminder_hour',
        ),
        migrations.RemoveField(
            model_name='smsconfiguration',
            name='same_day_reminder_hour',
        ),
        migrations.AddField(
            model_name='smsconfiguration',
            name='reminder_hour',
            field=models.IntegerField(default=20, help_text='ساعت ارسال پیامک یادآوری در روز قبل از ویزیت (0-23)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)], verbose_name='ساعت ارسال پیامک یادآوری'),
        ),
    ]
