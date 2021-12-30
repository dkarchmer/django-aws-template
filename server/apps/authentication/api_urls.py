from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import obtain_auth_token

from .api_views import APILoginViewSet, APILogoutViewSet, APITokenViewSet, APIUserInfoViewSet, FacebookLoginOrSignup

urlpatterns = [
    path('login/', APILoginViewSet.as_view(), name='api-login'),
    path('logout/', APILogoutViewSet.as_view(), name='api-logout'),
    path('token/', APITokenViewSet.as_view(), name='api-token'),
    path('user-info/', APIUserInfoViewSet.as_view(), name='api-user-info'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', csrf_exempt(obtain_auth_token), name='api-token-auth'),
    path('facebook-signup/?', csrf_exempt(FacebookLoginOrSignup.as_view()), name='facebook-login-signup'),
]
