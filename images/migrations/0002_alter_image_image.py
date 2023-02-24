# Generated by Django 4.1.7 on 2023-02-20 17:56

import django.core.validators
from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to=images.models.images_directory_path, validators=[django.core.validators.FileExtensionValidator(['PNG', 'JPG'])]),
        ),
    ]