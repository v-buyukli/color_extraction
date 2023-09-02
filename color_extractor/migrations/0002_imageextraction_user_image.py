from django.db import migrations, models

import color_extractor.services


class Migration(migrations.Migration):
    dependencies = [
        ("color_extractor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="imageextraction",
            name="user_image",
            field=models.ImageField(
                null=True, upload_to=color_extractor.services.upload_user_image
            ),
        ),
    ]
