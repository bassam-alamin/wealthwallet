# for now fetch the development settings only
from .development import *
from decouple import config

# turn off all debugging
DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = ["*"]

# SECURITY CONFIGURATION

# TODO: Make sure, that sensitive information uses https
# TODO: Evaluate the following settings, before uncommenting them
# redirects all requests to https
# SECURE_SSL_REDIRECT = True
# session cookies will only be set, if https is used
# SESSION_COOKIE_SECURE = True
# how long is a session cookie valid?
# SESSION_COOKIE_AGE = 1209600

# the email address, these error notifications to admins come from
SERVER_EMAIL = config('EMAIL_HOST_USER')

# how many days a password reset should work. I'd say even one day is too long
PASSWORD_RESET_TIMEOUT_DAYS = 1

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('PRIMARY_DB'),
        'USER': config('PRIMARY_DB_USER'),
        'HOST': config("PRIMARY_DB_HOST"),
        'PASSWORD': config("PRIMARY_DB_USER_PASSWORD"),
        'PORT': config("PRIMARY_DB_PORT"),
    }
}

# cache db details
CACHES = {
    "default": {
        "BACKEND": config("REDIS_BACKEND"),
        "LOCATION": config("REDIS_DB_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": config("REDIS_CLIENT_CLASS")
        },
        "KEY_PREFIX": "production"
    }
}

