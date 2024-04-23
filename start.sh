daphne -b 0.0.0.0 -p 8000 config.asgi:application
celery -A config.celery worker -l INFO