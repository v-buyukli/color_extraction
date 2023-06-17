from django.forms import ModelForm

from color_extractor.models import ImageExtraction


class StudentForm(ModelForm):
    class Meta:
        model = ImageExtraction
        fields = ("image_name", "user_image")
