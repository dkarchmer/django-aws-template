import logging

from django.contrib.auth import SESSION_KEY, get_user, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches
from django.db.models.signals import post_delete, post_save
from django.utils.functional import SimpleLazyObject

CACHE_KEY = 'cached_user:{0}'

# Get an instance of a logger
logger = logging.getLogger(__name__)

def invalidate_cache(sender, instance, **kwargs):
    if isinstance(instance, get_user_model()):
        key = CACHE_KEY.format(instance.id)
    else:
        key = CACHE_KEY.format(instance.user_id)
    logger.debug('Deleting User Cache: {0}'.format(key))
    cache = caches['default']
    cache.delete(key)


def get_cached_user(request):
    if not hasattr(request, '_cached_user'):
        try:
            key = CACHE_KEY.format(request.session[SESSION_KEY])
            cache = caches['default']
            user = cache.get(key)
        except KeyError:
            user = AnonymousUser()
        if user is None:
            user = get_user(request)
            cache = caches['default']
            # 8 hours
            cache.set(key, user, 28800)
            logger.debug('No User Cache. Setting now: {0}, {1}'.format(key, user.username))
        request._cached_user = user
    return request._cached_user


class CachedAuthenticationMiddleware(object):

    def __init__(self):
        post_save.connect(invalidate_cache, sender=get_user_model())
        post_delete.connect(invalidate_cache, sender=get_user_model())

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_cached_user(request))
