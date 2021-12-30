from django.urls import include, path

from .views import AccountDetailView, AccountRedirectView, AccountUpdateView

urlpatterns = [

     path('', include('allauth.urls')),
     path('', AccountRedirectView.as_view(), name='account_redirect'),
     path('<slug:slug>/edit/', AccountUpdateView.as_view(), name='account_edit'),
     path('<slug:slug>/', AccountDetailView.as_view(), name='account_detail'),
]
