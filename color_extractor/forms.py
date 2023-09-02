from django.forms import ModelForm

from color_extractor.models import ImageExtraction


class ImageExtractionForm(ModelForm):
    class Meta:
        model = ImageExtraction
        fields = ["user_image"]
