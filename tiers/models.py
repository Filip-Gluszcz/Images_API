from django.db import models
from django.contrib.auth.models import User
from images.models import Thumbnail


class Tier(models.Model):
    name = models.CharField(max_length=30)
    ori_img_link = models.BooleanField()
    expiring_link = models.BooleanField()
    thumbnails = models.ManyToManyField(Thumbnail, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)