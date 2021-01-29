import configparser
import os
from pathlib import Path

config = configparser.RawConfigParser()

if 'CHAOSINVENTORY_CONFIG_FILE' in os.environ:
    config.read_file(open(os.environ.get('CHAOSINVENTORY_CONFIG_FILE'), encoding='utf-8'))
else:
    config.read(['chaosinventory.cfg', '/etc/chaosinventory/chaosinventory.cfg'], encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'static'

SECRET_KEY = config.get('django', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('django', 'debug', fallback=False)

ALLOWED_HOSTS = config.get('django', 'allowed_hosts', fallback='*').split(',')


# Application definition

INSTALLED_APPS = [
    'chaosinventory.base',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chaosinventory.urls'

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

WSGI_APPLICATION = 'chaosinventory.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

database_backend = config.get('database', 'engine', fallback='sqlite3')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + database_backend,
        'NAME': config.get('database', 'name', fallback='db.sqlite3'),
        'USER': config.get('database', 'user', fallback=''),
        'PASSWORD': config.get('database', 'password', fallback=''),
        'HOST': config.get('database', 'host', fallback=''),
        'PORT': config.get('database', 'port', fallback=''),
        'CONN_MAX_AGE': 0 if database_backend == 'sqlite3' else 120
    }
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

LANGUAGE_CODE = config.get('django', 'language_code', fallback='en-us')

TIME_ZONE = config.get('django', 'time_zone', fallback='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.' + config.get('email', 'backend', fallback='filebased.EmailBackend')
EMAIL_FILE_PATH = config.get('email', 'file_path', fallback=BASE_DIR / 'emails')
EMAIL_HOST = config.get('email', 'host', fallback='')
EMAIL_PORT = config.get('email', 'port', fallback='')
EMAIL_HOST_USER = config.get('email', 'user', fallback='')
EMAIL_HOST_PASSWORD = config.get('email', 'password', fallback='')
EMAIL_USE_TLS = config.getboolean('email', 'tls', fallback=False)
EMAIL_USE_SSL = config.getboolean('email', 'ssl', fallback=False)
