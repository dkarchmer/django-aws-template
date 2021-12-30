from django.urls import include, path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
     path('', HomeIndexView.as_view(), name='home'),
     path('about/', AboutView.as_view(), name='about'),
     path('message/send/', ContactCreateView.as_view(), name='send-message'),
     # ---------------------------------
     path('jsi18n/', i18n_javascript),
     path('admin/jsi18n/', i18n_javascript),
     path('i18n/', include('django.conf.urls.i18n')),
     path('robots.txt', RobotView.as_view()),
     path('crossdomain.xml', CrossDomainView.as_view()),
]
