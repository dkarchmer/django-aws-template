"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers

from apps.authentication.api_views import AccountViewSet
from apps.main.api_views import APIMessageViewSet

# Rest APIs
# =========
v1_api_router = routers.DefaultRouter(trailing_slash=False)
v1_api_router.register(r'account', AccountViewSet)
v1_api_router.register(r'message', APIMessageViewSet)

admin.autodiscover()

urlpatterns = [

    url(r'^', include('apps.main.urls')),
    url(r'^account/', include('apps.authentication.urls')),

    url(r'^admin/', admin.site.urls),

    # Rest API
    url(r'^api/v1/', include(v1_api_router.urls)),
    url(r'^api/v1/auth/', include('apps.authentication.api_urls')),

]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
