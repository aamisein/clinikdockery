# Generated by Django 5.2.1 on 2025-05-09 15:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('INFO', 'اطلاعات'), ('WARNING', 'هشدار'), ('ERROR', 'خطا'), ('DEBUG', 'اشکال\u200cزدایی')], max_length=10, verbose_name='سطح')),
                ('message', models.TextField(verbose_name='پیام')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان')),
                ('module', models.CharField(max_length=100, verbose_name='ماژول')),
                ('task_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام تسک')),
            ],
            options={
                'verbose_name': 'لاگ',
                'verbose_name_plural': 'لاگ\u200cها',
                'ordering': ['-timestamp'],
            },
        ),
    ]
