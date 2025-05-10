import logging
from .models import LogEntry

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        try:
            LogEntry.objects.create(
                level=record.levelname,
                message=record.getMessage(),
                module=record.module,
                task_name=getattr(record, 'task_name', None)
            )
        except Exception:
            self.handleError(record) 