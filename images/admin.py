from django.contrib import admin
from .models import Image, Thumbnail


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']
