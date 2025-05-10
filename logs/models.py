from django.db import models
from django.utils import timezone

class LogEntry(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'اطلاعات'),
        ('WARNING', 'هشدار'),
        ('ERROR', 'خطا'),
        ('DEBUG', 'اشکال‌زدایی'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='سطح')
    message = models.TextField(verbose_name='پیام')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان')
    module = models.CharField(max_length=100, verbose_name='ماژول')
    task_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام تسک')

    class Meta:
        verbose_name = 'لاگ'
        verbose_name_plural = 'لاگ‌ها'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.message[:50]}"
