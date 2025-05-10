from celery import shared_task
from django.conf import settings
from visits.models import Visit, SMSConfiguration
from kavenegar import KavenegarAPI, APIException, HTTPException
import logging
from datetime import datetime, timedelta
import pytz

logger = logging.getLogger(__name__)

def get_sms_config():
    """دریافت تنظیمات پیامک"""
    try:
        return SMSConfiguration.objects.first()
    except Exception as e:
        logger.error(f"خطا در دریافت تنظیمات پیامک: {e}")
        return None

def send_sms(receptor, name, service_name, next_visit_date):
    """ارسال پیامک با استفاده از کاوه‌نگار"""
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'receptor': receptor,
            'template': 'visit-reminder',  # نام قالب ثبت شده در کاوه‌نگار
            'token': name,  # نام بیمار
            'token2': service_name,  # نام سرویس
            'token3': next_visit_date.strftime('%Y/%m/%d'),  # تاریخ ویزیت بعدی
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        logger.info(f"پیامک با موفقیت ارسال شد: {response}")
        return True
    except APIException as e:
        logger.error(f"خطای API کاوه‌نگار: {e}")
        return False
    except HTTPException as e:
        logger.error(f"خطای HTTP کاوه‌نگار: {e}")
        return False
    except Exception as e:
        logger.error(f"خطا در ارسال پیامک: {e}")
        return False

@shared_task
def send_visit_reminders():
    """ارسال پیامک یادآوری برای ویزیت‌های فردا"""
    sms_config = get_sms_config()
    if not sms_config or not sms_config.is_active:
        logger.info("ارسال پیامک غیرفعال است")
        return

    current_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
    if current_time.hour != sms_config.reminder_hour:
        return

    tomorrow = (current_time + timedelta(days=1)).date()
    visits = Visit.objects.filter(next_visit_date=tomorrow)
    
    for visit in visits:
        if send_sms(visit.phone, f"{visit.first_name} {visit.last_name}", visit.service.name, visit.next_visit_date):
            logger.info(f"پیامک یادآوری برای ویزیت {visit} ارسال شد")
        else:
            logger.error(f"خطا در ارسال پیامک یادآوری برای ویزیت {visit}")

