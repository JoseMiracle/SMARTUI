import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# Set the default Django settings module for the 'celery' program.
os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('smartui')  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'multiply-every-5-seconds': {
        'task': 'smartui.accounts.tasks.mul',
        'schedule': 5.0,
        'args': (16, 16)
    }

}