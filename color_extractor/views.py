from django.shortcuts import render

from color_extractor.models import ImageExtraction


def index(request):
    images = ImageExtraction.objects.all()
    return render(request, "index.html", {"images": images})
