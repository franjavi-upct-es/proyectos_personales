from django.apps import AppConfig
from apscheduler.schedulers.base import STATE_RUNNING

class OcrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ocr'

    def ready(self):
        from .tasks import scheduler
        # Arrancar sólo si no está corriendo
        if scheduler.state != STATE_RUNNING:
            scheduler.start()