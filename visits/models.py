from django.db import models
from jdatetime import datetime  # استفاده از jdatetime برای تاریخ شمسی
from django_jalali.db import models as jmodels
import jdatetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    first_name = models.CharField(max_length=100 ,verbose_name='نام')
    last_name = models.CharField(max_length=100 , verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11 ,verbose_name='شماره همراه')

    service = models.ForeignKey(Service, on_delete=models.CASCADE ,verbose_name=' خدمات')
    current_visit_date = jmodels.jDateField(verbose_name='تاریخ ویزیت')
    next_visit_date = jmodels.jDateField(verbose_name='تاریخ ویزیت بعدی', null=True, blank=True)
    SMS_sent = models.BooleanField(verbose_name='پیامک داده شده', default=False )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name}"

class SMSConfiguration(models.Model):
    reminder_hour = models.IntegerField(
        verbose_name='ساعت ارسال پیامک یادآوری',
        help_text='ساعت ارسال پیامک یادآوری در روز قبل از ویزیت (0-23)',
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        default=20
    )
    is_active = models.BooleanField(
        verbose_name='فعال',
        help_text='آیا ارسال پیامک فعال باشد؟',
        default=True
    )
    updated_at = models.DateTimeField(
        verbose_name='آخرین بروزرسانی',
        auto_now=True
    )

    class Meta:
        verbose_name = 'تنظیمات پیامک'
        verbose_name_plural = 'تنظیمات پیامک'

    def __str__(self):
        return f'تنظیمات پیامک (بروزرسانی: {self.updated_at.strftime("%Y-%m-%d %H:%M")})'

    def save(self, *args, **kwargs):
        if not self.pk and SMSConfiguration.objects.exists():
            return
        return super().save(*args, **kwargs)

   