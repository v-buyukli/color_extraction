from django.shortcuts import render

from color_extractor.models import ImageExtraction


def index(request):
    context = "Home page"
    return render(request, "index.html", {"context": context})


def add_image(request):
    pass

# images = ImageExtraction.objects.all()
