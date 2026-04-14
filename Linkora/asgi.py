"""
ASGI config for Linkora project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# your_project_name/asgi.py
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Linkora.settings')
django.setup()

# Import AFTER django.setup()
from chat.middleware import JwtAuthMiddleware
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP requests
    "http": get_asgi_application(),

    # WebSocket requests — removed AllowedHostsOriginValidator for dev
    "websocket": JwtAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})