from django.contrib import admin

from .forms import AdminUserChangeForm, AdminUserCreationForm
from .models import *


class AccountAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):

        if obj:
            return AdminUserChangeForm
        else:
            return AdminUserCreationForm

    list_display = ('id', 'username', 'email', 'name', 'created_at', 'last_login', 'is_active', 'is_staff')



"""
Register Admin Pages
"""
admin.site.register(Account, AccountAdmin)
