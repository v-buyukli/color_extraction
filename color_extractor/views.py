from django.shortcuts import render

from color_extractor.services import extract_colors


def index(request):
    # img_url = "http://surl.li/eyopf"

    # img_url = "https://file.liga.net/images/general/2020/09/08/20200908171549-5386.jpg?v=1599578314"
    # img_name = "test_image.jpg"
    # extract_colors(img_url, img_name)

    context = "Color Extraction page"
    return render(request, "index.html", {"context": context})
