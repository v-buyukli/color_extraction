from django.db import models

from color_extractor.services import upload_user_image


class ImageExtraction(models.Model):
    user_email = models.CharField(max_length=255, null=True)
    image_name = models.CharField(max_length=255, null=True)
    user_image = models.ImageField(
        upload_to=upload_user_image, null=True, verbose_name="Upload an image"
    )
