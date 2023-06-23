# Generated by Django 4.2.1 on 2023-06-17 12:12

from django.db import migrations, models

import color_extractor.models


class Migration(migrations.Migration):
    dependencies = [
        ("color_extractor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="imageextraction",
            name="user_image",
            field=models.ImageField(
                null=True, upload_to=color_extractor.models.upload_user_image
            ),
        ),
    ]
