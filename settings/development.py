
# project imports
from .common import *
# uncomment the following line to include i18n
from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
LOGIN_URL = "admin/login"
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "admin/login"


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('PRIMARY_DB'),
        'USER': config('PRIMARY_DB_USER'),
        'HOST': config("PRIMARY_DB_HOST"),
        'PASSWORD': config("PRIMARY_DB_USER_PASSWORD"),
        'PORT': config("PRIMARY_DB_PORT"),
        },
    'TEST': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DJANGO_ROOT, 'run', 'dev.sqlite3'),

    },
}

