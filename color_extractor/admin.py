from django.contrib import admin

from .models import ImageExtraction


class ImageExtractionAdmin(admin.ModelAdmin):
    list_display = ("user_email", "image_name", "user_image")
    list_filter = ("user_email", "image_name")
    search_fields = ("user_email", "image_name")


admin.site.register(ImageExtraction, ImageExtractionAdmin)
