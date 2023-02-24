from django.contrib import admin
from .models import Tier, Account

@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ['name', 'ori_img_link', 'expiring_link']
    list_editable = ['ori_img_link', 'expiring_link']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier']
    list_editable = ['tier']
    
