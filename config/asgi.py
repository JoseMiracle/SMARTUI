"""
ASGI config for smartui project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv
load_dotenv()

from django.core.asgi import get_asgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')
django_asgi_application = get_asgi_application()


from config import routing
from config.jwt_middleware import JWTAuthMiddleware  

# Defining the ASGI application with ProtocolTypeRouter
application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': JWTAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    }
)


