"""server URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

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

    path('', include('apps.main.urls')),
    path('account/', include('apps.authentication.urls')),

    path('admin/', admin.site.urls),

    # Rest API
    path('api/v1/', include(v1_api_router.urls)),
    path('api/v1/auth/', include('apps.authentication.api_urls')),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )
