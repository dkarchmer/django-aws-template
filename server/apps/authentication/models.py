"""
Custom User Model
"""

import hashlib
import logging
import os
# import code for encoding urls and generating md5 hashes
import urllib.parse
import uuid

import pytz

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify

from allauth.account.signals import user_signed_up
from rest_framework.authtoken.models import Token

from .tasks import send_new_user_notification

# Get an instance of a logger
logger = logging.getLogger(__name__)


def new_sign_up(sender, **kwargs):
    account = kwargs['user']
    logger.info('A new user has signed up! - {username}'.format(username=account.username))
    logger.debug('--> New User: ' + str(account))
    send_new_user_notification(id=account.id, username=account.username, email=account.email)

    '''
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    '''

    if not 'sociallogin' in kwargs:
        return

    social_login = kwargs['sociallogin']
    print('user is ' + str(account))
    if social_login:
        print(str(social_login.account.provider))
        print(str(social_login.account.extra_data))
        # Extract first / last names from social nets and store on User record
        if social_login.account.provider == 'twitter':
            if 'name' in social_login.account.extra_data:
                account.name = social_login.account.extra_data['name']

        if social_login.account.provider == 'facebook':
            name = ''
            if 'first_name' in social_login.account.extra_data:
                first_name = social_login.account.extra_data['first_name']
                name = first_name
            if 'last_name' in social_login.account.extra_data:
                last_name = social_login.account.extra_data['last_name']
                if name != '':
                    name += ' '
                name += last_name

            account.name = name

        if social_login.account.provider == 'google':
            if 'name' in social_login.account.extra_data:
                account.name = social_login.account.extra_data['name']
            if 'picture' in social_login.account.extra_data:
                account.external_avatar_url = social_login.account.extra_data['picture']

        account.save()


# Connect django-allauth Signals
user_signed_up.connect(new_sign_up)


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.access_level = 0
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.is_active = True
        account.is_staff = True
        account.save()

        return account


class Account(AbstractBaseUser):

    TZ_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    name = models.CharField(verbose_name='Full Name', max_length=120, blank=True)
    tagline = models.CharField(max_length=260, blank=True)

    external_avatar_url = models.CharField(max_length=260, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    time_zone = models.CharField(max_length=64, null=True, default=settings.TIME_ZONE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['slug']

    def save(self, *args, **kwargs):

        slug = slugify(self.username)
        self.slug = slug
        count = 0
        while Account.objects.filter(slug=self.slug).exclude(pk=self.id).exists():
            self.slug = '{0}{1}'.format(slug, count)
            logger.debug('Slug conflict. Trying again with {0}'.format(self.slug))
            count += 1

        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return '@{0}'.format(self.username)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if (self.name != ''):
            # Try to extract the first name
            names = self.name.split()
            first_name = names[0]
            return first_name
        return self.username

    # For full access to Permission system, we needed to add the PermissionMixin
    def has_perm(self, perm, obj=None):
        return True

    def has_perms(perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Custom Methods
    # --------------
    def get_absolute_url(self):
        return '/account/%s/' % self.slug

    def get_edit_url(self):
        return '%sedit/' % self.get_absolute_url()

    def get_token(self):
        try:
            token = Token.objects.get(user=self)
        except:
            token = Token.objects.create(user=self)
        return token

    def get_gravatar_thumbnail_url(self, size=100):
        # Set your variables here
        email = self.email
        default = 'identicon'

        # construct the url
        gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
        try:
            # Python 3.4
            gravatar_url += urllib.parse.urlencode({'d': default, 's': str(size)})
        except:
            # Python 2.7
            gravatar_url += urllib.urlencode({'d': default, 's': str(size)})

        return gravatar_url
