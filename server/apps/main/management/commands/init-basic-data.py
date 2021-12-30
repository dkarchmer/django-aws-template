from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp

from apps.authentication.models import Account


class Command(BaseCommand):

    def _create_super_users(self):
        for user in getattr(settings, 'ADMINS'):
            username = user[0].replace(' ', '')
            email = user[1]
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = Account.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            EmailAddress.objects.create(email=email, user=admin, verified=True, primary=True)

    def _create_social_accounts(self, site):
        # For test/stage, also create dummy Facebook setup
        print('Creating Dummy SocialApp for Facebook')
        app = SocialApp.objects.create(provider='facebook',
                                       name='Facebook',
                                       client_id='Foo',
                                       secret='Bar'
                                       )
        app.sites.add(site)
        app.save()
        app = SocialApp.objects.create(provider='twitter',
                                       name='Twitter',
                                       client_id='Foo',
                                       secret='Bar'
                                       )
        app.sites.add(site)
        app.save()
        app = SocialApp.objects.create(provider='google',
                                       name='Google',
                                       client_id='Foo',
                                       secret='Bar'
                                       )
        app.sites.add(site)
        app.save()

    def handle(self, *args, **options):

        if Account.objects.count() == 0:
            # If there are no Accounts, we can assume this is a new Env
            # create a super user
            self._create_super_users()

        if SocialApp.objects.count() == 0:
            # Also fixup  the Site info
            site = Site.objects.get_current()
            site.domain_name = getattr(settings, 'DOMAIN_NAME')
            site.display_name = getattr(settings, 'COMPANY_NAME')
            site.save()
            if not getattr(settings, 'PRODUCTION'):
                self._create_social_accounts(site)

        else:
            print('Admin accounts can only be initialized if no Accounts exist')
