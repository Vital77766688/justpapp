import os, dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY'] # 'fw4fli3wm-0c(r)u(_9tblo(m)m=b(s(ywp39m8+1y37q%)2%^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'corsheaders',

    'accounts',
    'chat',

]

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# CSRF_COOKIE_SAMESITE = None
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = None
# SESSION_COKIE_SECURE = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True

ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'accounts.serializers.PasswordResetSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserDetailsSerializer',
    'TOKEN_SERIALIZER': 'accounts.serializers.TokenSerializer',
}

OLD_PASSWORD_FIELD_ENABLED = True

EMAIL_CONFIRMATION_SIGNUP = 'accounts/emails/email_confirmation_signup'
EMAIL_CONFIRMATION = 'accounts/emails/email_confirmation'
PASSWORD_RESET_SUBJECT_TEMPLATE = 'accounts/emails/password_reset_key_subject.txt'
PASSWORD_RESET_EMAIL_TEMPLATE = 'accounts/emails/password_reset_key_message.txt'

ROOT_URLCONF = 'dj.urls'
DEFAULT_FROM_EMAIL = 'noreply@example.com'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
     {
         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
     },
     {
         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     },
     {
         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
     },
     {
         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
     },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/build/static')
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')