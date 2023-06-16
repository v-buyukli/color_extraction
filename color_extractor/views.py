from django.shortcuts import render


def index(request):
    context = "Color Extraction page"
    return render(request, "index.html", {"context": context})
