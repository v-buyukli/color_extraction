from django.db import models


class ImageExtraction(models.Model):
    image_name = models.CharField(max_length=255)
