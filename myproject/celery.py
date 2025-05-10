from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# تنظیم متغیر محیطی DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# استفاده از تنظیمات جنگو برای پیکربندی Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# بارگذاری خودکار تسک‌ها از همه فایل‌های tasks.py در اپلیکیشن‌های ثبت شده
app.autodiscover_tasks()

# تنظیم زمان‌بندی تسک‌ها
app.conf.beat_schedule = {
    'check-and-send-visit-reminders': {
        'task': 'myproject.tasks.send_visit_reminders',
        'schedule': crontab(minute=0),  # اجرا در ابتدای هر ساعت
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 