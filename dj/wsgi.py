"""
WSGI config for dj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings = os.environ.get('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings if settings else 'dj.settings.settings_development')

application = get_wsgi_application()
