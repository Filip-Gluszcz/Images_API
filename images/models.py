from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def images_directory_path(instance, filename):
    '''
    Sets a path to the image including filename.
    '''
    return f'images/{filename}'


class Image(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=images_directory_path, default='images/default.jpg', validators=[FileExtensionValidator(['PNG', 'JPG'])])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Thumbnail(models.Model):
    name = models.CharField(max_length=50)
    size = models.IntegerField(default=100)

    def __str__(self):
        return self.name