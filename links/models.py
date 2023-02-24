from django.db import models
from images.models import Image
from django.core.validators import MaxValueValidator, MinValueValidator 

class ExpiringLink(models.Model):
    code = models.CharField(max_length=30)
    expire_after = models.IntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)])
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default='2023-02-21 15:43:51.575532')

    def __str__(self):
        return self.code