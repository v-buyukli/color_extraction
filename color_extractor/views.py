from django.shortcuts import render, redirect
from django.urls import reverse

from color_extractor.forms import ImageExtractionForm
from color_extractor.models import ImageExtraction


def images(request):
    images_list = ImageExtraction.objects.all().order_by("-id")
    return render(request, "images.html", {"images_list": images_list})


def index(request):
    context = "Home page"
    return render(request, "index.html", {"context": context})


def add_image(request):
    form = ImageExtractionForm(request.POST or None, request.FILES or None)

    if request.method == "GET":
        return render(request, "add_image.html", {"form": form})
    if form.is_valid():
        form.save()
        return redirect(reverse(images))
    return render(request, "add_image.html", {"form": form})
