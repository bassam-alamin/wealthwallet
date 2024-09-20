# Python imports
import os
import sys
from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath

from celery.schedules import crontab
from decouple import config
from django.contrib.messages import constants as message_constants
from rest_framework.settings import api_settings


# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.normpath(os.path.dirname(__file__))

# # fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)
#
# # collect static files here
STATIC_ROOT = join(DJANGO_ROOT, 'run', )
#
# # collect media files here
MEDIA_ROOT = join(DJANGO_ROOT, 'run', 'media')

# # logs folder
LOGS_ROOT = join(DJANGO_ROOT, 'logs')
#
# look for static assets here
STATICFILES_DIRS = [
    join(STATIC_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(DJANGO_ROOT, 'run', 'templates'),
]
#
# add apps/ to the Python path
sys.path.append(normpath(join(DJANGO_ROOT, 'apps')))

# ##### APPLICATION CONFIGURATION #########################

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    # custom apps
    "apps.auth_app",
    "apps.investments",
    "apps.platform_admin"

]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'django_celery_results',
    'drf_yasg',
    'corsheaders',
    'rangefilter',
    'django_filters',
    'knox',

]

# swagger settings
REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'BasicAuth': {
            'type': 'basic',
            'description': 'Basic Authentication. Enter your username and password.'
        }
    },
    'SECURITY_REQUIREMENTS': [
        {
            'Bearer': [],
            'BasicAuth': []
        }
    ],
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
        'drf_yasg.inspectors.JSONFieldInspector',
        'drf_yasg.inspectors.HiddenFieldInspector',
        'drf_yasg.inspectors.RecursiveFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
    ],
}

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = ['Cross-Origin-Opener-Policy']

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

            ],
        },
    },
]

# Internationalization
USE_I18N = False

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(DJANGO_ROOT, 'run', 'SECRET.key'))



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'knox.auth.TokenAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        # Any other renders
    ),
    'DEFAULT_PARSER_CLASSES': (
        # If you use MultiPartFormParser or FormParser
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # Any other parsers
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# ##### PROFILER CONFIGURATION #########################
SILKY_PYTHON_PROFILER = True
SITE_ID = 1

# ENVIRONMENT CONFIGURATION
ENVIRONMENT_NAME = config('ENVIRONMENT_NAME', "localhost")
ENVIRONMENT_COLOR = config('ENVIRONMENT_COLOR', "green")

# MESSAGING CONFIGURATION

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_LEVEL = 10  # DEBUG

# COOKIE CONFIGURATION
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# LOGGING CONFIGURATION
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s"
                      " [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        "stdOut": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard"
        },
        "stdErr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "standard"
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_ROOT + "/logs.log",
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 31,  # how many backup file to keep, 10 days
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stdOut'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['stdOut', 'stdErr'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'investment_views': {
            'handlers': ['console', 'logfile', 'stdOut', 'stdErr'],
            'level': 'INFO',
            'propagate': True,
        },
        'auth_app_views': {
            'handlers': ['console', 'logfile', 'stdOut', 'stdErr'],
            'level': 'INFO',
            'propagate': True,
        },
        'platform_admin_views': {
            'handlers': ['console', 'logfile', 'stdOut', 'stdErr'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# finally grab the SECRET KEY

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string

        chars = config("SECURITY_KEY")
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)

AUTH_USER_MODEL = 'auth_app.User'

# APPLICATION CONFIGURATION
INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FCM_DJANGO_SETTINGS = {
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "firebase cloud messaging",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}

CACHES = {
    "default": {
        "BACKEND": config("REDIS_BACKEND", "django_redis.cache.RedisCache"),
        "LOCATION": config("REDIS_DB_LOCATION", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": config("REDIS_CLIENT_CLASS", "django_redis.client.DefaultClient")
        },
        "KEY_PREFIX": "development"
    }
}

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(hours=10),
    'USER_SERIALIZER': 'apps.auth_app.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}
