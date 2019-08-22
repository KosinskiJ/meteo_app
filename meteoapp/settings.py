import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'adasdasdasjda;idljasldjakhfgklrglksjgfkljsgksjgha'
ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # external apps
    'debug_toolbar',
    'crispy_forms',
    'polymorphic',

    # my apps
    'dashboard',
    'forecaster',
    'client',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'meteoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'meteoapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'meteoapp',
    #     'USER': 'wojtech',
    #     'PASSWORD': 'wojtech',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

TIME_ZONE = 'Europe/Warsaw'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

AUTH_USER_MODEL = 'dashboard.User'
# should be in development.settings.py
INTERNAL_IPS = ['127.0.0.1']
LOGIN_REDIRECT_URL = '/login-redirect/'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'task-number-one': {
        'task': 'client.celery.change_weather_forecast_statuses',
        'schedule': 1.0,
    },
}

import django_heroku

django_heroku.settings(locals())
