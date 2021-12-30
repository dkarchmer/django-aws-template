import json
import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, RedirectView, TemplateView, View
from django.views.generic.edit import FormView, UpdateView

from .forms import *
from .models import Account

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AccountRedirectView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        return HttpResponseRedirect(reverse('account_detail', args=(user.username,)))


class AccountDetailView(DetailView):
    model = Account
    template_name = 'authentication/detailVCard.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['referer'] = self.request.META.get('HTTP_REFERER')
        context['is_owner'] = (self.object == self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountDetailView, self).dispatch(request, *args, **kwargs)


class AccountThumbnailView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(Account, slug=kwargs['slug'])
        return user.get_thumbnail_url()


class AccountTinyView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(Account, slug=kwargs['slug'])
        return user.get_tiny_url()


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.time_zone = form.cleaned_data.get('time_zone')
        self.object.save()

        # Update session as well
        self.request.session['django_timezone'] = str(form.cleaned_data.get('time_zone'))

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(**kwargs)
        context['referer'] = self.request.META.get('HTTP_REFERER')

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountUpdateView, self).dispatch(request, *args, **kwargs)


