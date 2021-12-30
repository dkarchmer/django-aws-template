# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=config.settings.production
import logging.config
import socket

from .base import *  # NOQA

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = False

enable_security = True
if enable_security:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    '''
    The following comes from:
    http://security.stackexchange.com/questions/8964/trying-to-make-a-django-based-site-use-https-only-not-sure-if-its-secure/8970#comment80472_8970
    '''
    os.environ['HTTPS'] = "on"
    # Must mention ALLOWED_HOSTS in production!
    local_ip = str(socket.gethostbyname(socket.gethostname()))
    print ('hostname: ' + socket.gethostname())
    print ('hostbyname: ' + local_ip)

    # ALLOWED_HOSTS=[local_ip, '.mydomain.com', 'myapp.elasticbeanstalk.com' ]
else:
    ALLOWED_HOSTS = ['*', ]
    print('**********************************')
    print('**********************************')
    print('WARNING: Disable security features')
    print('**********************************')
    print('**********************************')


# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_BUCKET_NAME = env.str('AWS_MEDIA_BUCKET_NAME')

# Define STATIC_ROOT for the collectstatic command
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Setup CloudFront
AWS_S3_URL_PROTOCOL = 'https'
# Enable one AWS_S3_CUSTOM_DOMAIN to use cloudfront
# AWS_S3_CUSTOM_DOMAIN = 'xxxxxxx.cloudfront.net'
AWS_S3_CUSTOM_DOMAIN = 'cdn.mydomain.com'
# STATIC_URL = S3_STATIC_URL + STATIC_DIRECTORY - Use to host statics on S3 only
STATIC_URL = AWS_S3_URL_PROTOCOL + "://" + AWS_S3_CUSTOM_DOMAIN + '/static/'

