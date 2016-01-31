"""
Django Admin setup for the RSSNext project models.
"""

from django.contrib import admin
from .models import Subscription, EntryRelation, UserStatus

admin.site.register(Subscription)
admin.site.register(EntryRelation)
admin.site.register(UserStatus)
