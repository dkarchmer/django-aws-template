from .base import *             # NOQA
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': True})

TIME_ZONE = 'US/Pacific'

STATIC_ROOT = str(ROOT_DIR.path('staticfiles'))
STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = (
 ('dist', os.path.join(STATIC_ROOT, 'dist')),
)

LOGGING['loggers']['']['level'] = 'WARNING'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.sqlite',
    }
}
print(str(DATABASES))

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Debug Toolbar (http://django-debug-toolbar.readthedocs.org/)
# By default (for development), show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django_ses.SESBackend'
print('EMAIL_BACKEND = {0}'.format(EMAIL_BACKEND))

CORS_ORIGIN_WHITELIST += ('http://localhost:8000',)

# Kinesis Firehose:
# -----------------
USE_FIREHOSE = False




