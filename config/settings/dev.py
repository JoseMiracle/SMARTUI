from .base import *


LOCAL_APPS = [
    "smartui.accounts",
    "smartui.chats",
    "smartui.medicals"
] 


THIRD_PARTY_APPS = [
    "channels",
    'rest_framework',
    "django_celery_beat",
    "drf_standardized_errors",
]


INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS


# CHANNELS_SETTINGS
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# SIMPLE JWT SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# CELERY SETTINGS

CELERY_BROKER_URL = os.getenv('CELERY_BROKER', "redis://redis:6379/0" )
CELERY_RESULT_BACKEND = os.getenv('CELEEY_RESULT_BACKEND', "redis://redis:6379/0")


# schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


# E-MAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')