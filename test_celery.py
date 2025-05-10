import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myproject.tasks import calculate_factorial
from celery.result import AsyncResult
import time

# اجرای تسک
result = calculate_factorial.delay(5)
print(f"Task ID: {result.id}")

# صبر کردن برای اتمام تسک
time.sleep(3)  # صبر کردن بیشتر از 2 ثانیه برای اطمینان از اتمام تسک

# بررسی نتیجه
task_result = AsyncResult(result.id)
print(f"Task Status: {task_result.status}")
print(f"Task Result: {task_result.result}") 