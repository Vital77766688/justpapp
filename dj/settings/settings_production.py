import os, dj_database_url
from .settings_base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True

DATABASES = {
    'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
}
