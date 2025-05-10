from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'module', 'task_name', 'message')
    list_filter = ('level', 'module', 'task_name')
    search_fields = ('message', 'module', 'task_name')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False  # جلوگیری از اضافه کردن لاگ به صورت دستی
    
    def has_change_permission(self, request, obj=None):
        return False  # جلوگیری از ویرایش لاگ‌ها
