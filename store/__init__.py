# импорт Celery приложения
from gameshop.celery_app import app as celery_app

__all__ = ('celery_app',)
