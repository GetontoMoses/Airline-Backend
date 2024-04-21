"""Admin configuration for Student app."""

from django.contrib import admin
from .models import upload

admin.site.register(upload)
