# 
from django.contrib import admin
from .models import Visit, Service, SMSConfiguration
from jalali_date.admin import ModelAdminJalaliMixin

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Visit)
class VisitAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'current_visit_date', 'next_visit_date', 'service']
    list_filter = ['service', 'current_visit_date', 'next_visit_date']
    search_fields = ['first_name', 'last_name', 'phone']

@admin.register(SMSConfiguration)
class SMSConfigurationAdmin(admin.ModelAdmin):
    list_display = ('reminder_hour', 'is_active', 'updated_at')
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # فقط یک نمونه از تنظیمات می‌تواند وجود داشته باشد
        return not SMSConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # نباید تنظیمات را حذف کرد
        return False