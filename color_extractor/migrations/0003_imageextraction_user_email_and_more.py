from django.db import migrations, models

import color_extractor.services


class Migration(migrations.Migration):
    dependencies = [
        ("color_extractor", "0002_imageextraction_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="imageextraction",
            name="user_email",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="imageextraction",
            name="image_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="imageextraction",
            name="user_image",
            field=models.ImageField(
                null=True,
                upload_to=color_extractor.services.upload_user_image,
                verbose_name="Upload an image",
            ),
        ),
    ]
