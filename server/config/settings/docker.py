from .base import *             # NOQA
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': True})

STATIC_URL = '/static/'
STATIC_ROOT = '/www/static/'
STATICFILES_DIRS = (
    ('dist', os.path.join(STATIC_ROOT, 'dist')),
)

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Debug Toolbar (http://django-debug-toolbar.readthedocs.org/)
INSTALLED_APPS += ('debug_toolbar',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1', '192.168.99.100',)
DEBUG_TOOLBAR_PANELS = [
 'debug_toolbar.panels.versions.VersionsPanel',
 'debug_toolbar.panels.timer.TimerPanel',
 'debug_toolbar.panels.settings.SettingsPanel',
 'debug_toolbar.panels.headers.HeadersPanel',
 'debug_toolbar.panels.request.RequestPanel',
 'debug_toolbar.panels.sql.SQLPanel',
 # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
 'debug_toolbar.panels.templates.TemplatesPanel',
 'debug_toolbar.panels.signals.SignalsPanel',
 'debug_toolbar.panels.logging.LoggingPanel',
 'debug_toolbar.panels.redirects.RedirectsPanel',
]

