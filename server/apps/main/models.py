import mimetypes
import os

from django.db import models


class ContactMessage(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()

    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name






