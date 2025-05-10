from django.apps import AppConfig
from django.conf import settings
import logging


class LogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logs'

    def ready(self):
        # Add database handler after Django is fully loaded
        if not settings.DEBUG:  # Only add database handler in production
            logging_config = settings.LOGGING
            logging_config['handlers']['database'] = {
                'class': 'logs.handlers.DatabaseHandler',
                'formatter': 'verbose',
            }
            logging_config['root']['handlers'].append('database')
            logging_config['loggers']['myproject']['handlers'].append('database')
            logging.config.dictConfig(logging_config)
