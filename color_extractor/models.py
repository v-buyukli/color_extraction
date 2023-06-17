import uuid

from django.db import models


def upload_user_image(instance, filename):
    return f"user_images/{uuid.uuid4()}/{filename}"


class ImageExtraction(models.Model):
    image_name = models.CharField(max_length=255)
    user_image = models.ImageField(upload_to=upload_user_image, null=True)
