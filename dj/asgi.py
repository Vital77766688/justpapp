"""
ASGI config for dj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings = os.environ.get('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings if settings else 'dj.settings.settings_development')

application = get_asgi_application()
