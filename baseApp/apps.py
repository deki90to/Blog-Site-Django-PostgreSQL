from django.apps import AppConfig
from django.db.models import signals


class BaseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baseApp'
    
    # Signals
    def ready(self):
        import baseApp.signals
