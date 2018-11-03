
import logging
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, CreateView
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .models import *
from .forms import *
from .tasks import send_contact_me_notification

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomeIndexView(TemplateView):

    def get_template_names(self):
        user = self.request.user

        if user.is_authenticated():
            template_name = 'main/index.html'
        else:
            template_name = 'main/landing.html'

        return template_name

    def get_context_data(self, **kwargs):
        context = super(HomeIndexView, self).get_context_data(**kwargs)

        context['production'] = settings.PRODUCTION
        context['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
        context['user'] = self.request.user

        return context


class RobotView(TemplateView):
    template_name = 'robots.txt'


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


class CrossDomainView(TemplateView):
    template_name = 'crossdomain.xml'

    def get_context_data(self, **kwargs):
        context = super(CrossDomainView, self).get_context_data(**kwargs)
        domains = []
        host = self.request.get_host()
        if host:
            domains.append(host)
        cdn = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
        if cdn:
            domains.append(cdn)

        context['extra_domains'] = domains

        return context


class ContactCreateView(CreateView):
    model = ContactMessage
    template_name = 'newForm.html'

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return ContactPrivateForm
        return ContactPublicForm

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['referer'] = self.request.META.get('HTTP_REFERER')
        else:
            context['referer'] = '/'
        context['title'] = _('Send us a message')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        if self.request.user.is_authenticated():
            self.object.name = self.request.user.name
            self.object.email = self.request.user.email
            self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Your message has been sent.')

        return HttpResponseRedirect('/')


class AboutView(TemplateView):
    template_name = 'main/about.html'