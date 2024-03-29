import configparser
import os
import logging
from pathlib import Path
import secrets

config = configparser.RawConfigParser()
secret_generated = False

try:
    if 'CHAOSINVENTORY_CONFIG_FILE' in os.environ:
        # Use read to avoid failing when file is not existing. This allows for auto creation in the given directory.
        config.read(os.environ.get('CHAOSINVENTORY_CONFIG_FILE', ''), encoding='utf-8')
    else:
        config.read(['chaosinventory.cfg', '/etc/chaosinventory/chaosinventory.cfg'], encoding='utf-8')
except configparser.Error as e:
    logging.critical((
        '{0} occured while parsing the configuration at {1}:{2}:\n'
        '{3}\nNote: {4}'
    ).format(
        type(e).__name__,
        e.source,
        e.lineno,
        e,
        type(e).__doc__.splitlines()[0]
    ))
    exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'static'
APP_ROOT = BASE_DIR / 'project-static' / 'dist'

SECRET_KEY = config.get('django', 'secret', fallback=None)

if SECRET_KEY is None:
    logging.warn("No custom secret configured. New random secret will be generated!")
    # random secret will be generated. This key may be persisted in the next section
    SECRET_KEY = secrets.token_urlsafe()
    secret_generated = True

if not len(config.sections()):
    # persist generated secret key
    config.add_section('django')
    config.set('django', 'secret', SECRET_KEY)

    # decide where to store the autogenerated configuration file
    conffile = os.path.abspath(os.environ.get('CHAOSINVENTORY_CONFIG_FILE', 'chaosinventory.cfg'))
    logging.warn(
        "No custom configuration file was provided! "
        "Continuing with example values. "
        f"Conffile with secrets will be written to {conffile}, make sure to keep it!"
    )
    with open(conffile, 'w') as configfile:
        config.write(configfile)
else:
    if secret_generated:
        logging.error(
            "Configuration file was loaded with no secret set! "
            "Please configure a secret manually in your configuration files django section, and restart!")
        exit(1)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('django', 'debug', fallback=False)

ALLOWED_HOSTS = config.get('django', 'allowed_hosts', fallback='*').split(',')

CORS_ALLOWED_ORIGINS = config.get('django', 'cors_allowed_origins', fallback='http://localhost').split(',')
CORS_ALLOW_ALL_ORIGINS = config.getboolean('django', 'cors_allow_all', fallback=False)

# Application definition

INSTALLED_APPS = [
    'chaosinventory.base',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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
# Prioritizing env variables over config files
database_backend = os.environ.get('CHAOSINVENTORY_DB_ENGINE', config.get('database', 'engine', fallback='sqlite3'))
database_name = os.environ.get('CHAOSINVENTORY_DB_NAME', config.get('database', 'name', fallback='db.sqlite3'))
database_user = os.environ.get('CHAOSINVENTORY_DB_USER', config.get('database', 'user', fallback=''))
database_password = os.environ.get('CHAOSINVENTORY_DB_PASSWORD', config.get('database', 'password', fallback=''))
database_host = os.environ.get('CHAOSINVENTORY_DB_HOST', config.get('database', 'host', fallback=''))
database_port = os.environ.get('CHAOSINVENTORY_DB_PORT', config.get('database', 'port', fallback=''))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + database_backend,
        'NAME': database_name,
        'USER': database_user,
        'PASSWORD': database_password,
        'HOST': database_host,
        'PORT': database_port,
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = "/"
