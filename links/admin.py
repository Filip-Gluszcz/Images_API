from django.contrib import admin
from .models import ExpiringLink

@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
    list_display = ['image', 'code', 'expire_after']


