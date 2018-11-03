"""
Django settings for {{ project_name }} project.
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import sys

# Use 12factor inspired environment variables or from a file
import environ

from django.urls import reverse_lazy
from django.contrib import messages


# Build paths inside the project like this: join(BASE_DIR, "directory")
BASE_PATH = environ.Path(__file__) - 3
BASE_DIR = str(BASE_PATH)
LOG_FILE = BASE_PATH.path('logs')
print('BASE_DIR = ' + BASE_DIR)

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    RECAPTCHA_PUBLIC_KEY=(str, 'Changeme'),
    RECAPTCHA_PRIVATE_KEY=(str, 'Changeme'),
    PRODUCTION=(bool, False),
    DOMAIN_NAME=(str, 'mydomain.com'),
    DOMAIN_BASE_URL=(str, 'https://mydomain.com'),
    COMPANY_NAME=(str, 'COMPANY_NAME'),
    INITIAL_ADMIN_EMAIL=(str, 'admin@mydomain.com'),
    DJANGO_ENV_FILE = (str, '.local.env')
)

SITE_ID = 1

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
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

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = os.path.join(os.path.dirname(__file__), env('DJANGO_ENV_FILE'))

if os.path.isfile(env_file):
    print('Reading Env file: {0}'.format(env_file))
    environ.Env.read_env(env_file)
else:
    print('Warning!! No .env file: {0}'.format(env_file))

ADMINS = (
    # ('Username', 'your_email@domain.com'),
    ('admin', env('INITIAL_ADMIN_EMAIL')),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []

PRODUCTION = env('PRODUCTION')
DOMAIN_NAME = env('DOMAIN_NAME')
COMPANY_NAME = env('COMPANY_NAME')

# Application definition

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'captcha',
    'crispy_forms',
)

# Apps specific for this project go here.
COMMON_APPS = (
    'apps.authentication',
    'apps.main',
)

INSTALLED_APPS = DJANGO_APPS + COMMON_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.utils.timezoneMiddleware.TimezoneMiddleware',
)


ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
            'CONN_MAX_AGE': 600,
        }
    }
else:
    DATABASES = {
        # Raises ImproperlyConfigured exception if DATABASE_URL not in
        # os.environ
        'default': env.db(),
    }

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

ROOT_DIR = environ.Path(__file__) - 4
STATIC_ROOT = str(ROOT_DIR.path('staticfiles'))
STATICFILES_DIRS = []

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Crispy Form Theme - Bootstrap 3
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Authentication Settings
AUTH_USER_MODEL = 'authentication.Account'
#LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
#LOGIN_URL = reverse_lazy("accounts:login")

# Recaptcha https://www.google.com/recaptcha/admin
# https://github.com/praekelt/django-recaptcha
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True

# https://github.com/ottoyiu/django-cors-headers/
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api.*$'
CORS_ORIGIN_WHITELIST = (
    'mydomain.com',
    'xxxxxxxxxx.cloudfront.net',
)

CSRF_COOKIE_HTTPONLY = False # Most be False for javascript APIs to be able to post/put/delete
SESSION_COOKIE_HTTPONLY = True

# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'apps.utils.pagination.StandardResultsSetPagination'
}

# auth and allauth settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL          = '/account/login/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
#SOCIALACCOUNT_EMAIL_REQUIRED = False
'''
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile'],
        #'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'VERSION': 'v2.4',
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
        ],
    },
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': { 'access_type': 'online' }
    }
}
'''
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD= 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {
    'login': 'apps.authentication.forms.AllauthLoginForm',
    'signup': 'apps.authentication.forms.AllauthSignupForm'
}

if PRODUCTION:
    # For production, hard code to file created by .ebextensions
    LOG_FILEPATH = '/opt/python/log/my.log'
else:
    LOG_FILEPATH = os.path.join(str(LOG_FILE), 'server.log')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILEPATH,
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'simple'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

if not PRODUCTION:
    print('PRODUCTION=False')
    AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')

    # BOTO may need an actual Env Variable, so set it
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

TEST_RUNNER = 'config.runner.AppsTestSuiteRunner'