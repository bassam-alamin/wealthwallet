# Python imports
from os.path import join

# Django imports
from django.utils.translation import gettext_lazy as _

# project imports
from .common import PROJECT_ROOT, MIDDLEWARE

# ##### INTERNATIONALIZATION ##############################

LANGUAGE_CODE = 'en-us'
# Internationalization
USE_I18N = True

# Localisation
USE_L10N = True

TIME_ZONE = 'Africa/Nairobi'
USE_TZ = False
DJANGO_CELERY_BEAT_TZ_AWARE = False

# This list of languages will be provided
LANGUAGES = (
    ('en', _('English')),
    ('de', _('German'))
)

# Look for translations in these locations
LOCALE_PATHS = (
    join(PROJECT_ROOT, 'locale'),
)

# Inject the localization middleware into the right position
MIDDLEWARE = [y for i, x in enumerate(MIDDLEWARE) for y in (
    ('django.middleware.locale.LocaleMiddleware', x)
    if MIDDLEWARE[i - 1] == 'django.contrib.sessions.'
                            'middleware.SessionMiddleware'
    else (x,))]
