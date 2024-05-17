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
    "drf_spectacular",
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




SPECTACULAR_SETTINGS = {
    'TITLE': 'SMART HEALTHCARE DOCS',
    'DESCRIPTION': 'HEALTHCARE MANAGEMENT SYSTEM',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# CELERY SETTINGS

CELERY_BROKER_URL = os.getenv('CELERY_BROKER', os.getenv('REDIS_URL') )
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', os.getenv('REDIS_URL'))


# schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


# E-MAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')