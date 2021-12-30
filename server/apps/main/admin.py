from django.contrib import admin

from .models import *


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


"""
Register Admin Pages
"""
admin.site.register(ContactMessage, ContactMessageAdmin)
