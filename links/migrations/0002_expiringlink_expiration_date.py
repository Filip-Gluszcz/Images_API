# Generated by Django 4.1.7 on 2023-02-21 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expiringlink',
            name='expiration_date',
            field=models.DateTimeField(default='2023-02-21 15:43:51.575532'),
        ),
    ]