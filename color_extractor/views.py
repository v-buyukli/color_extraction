import json
from urllib.parse import quote_plus, urlencode

import requests
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from color_extractor.forms import ImageExtractionForm
from color_extractor.models import ImageExtraction


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):
    s = request.session.get("user")
    return render(
        request,
        "index.html",
        context={
            "session": s,
            "pretty": json.dumps(s, indent=4),
        },
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def images(request):
    images_list = ImageExtraction.objects.all().order_by("-id")
    return render(request, "images.html", {"images_list": images_list})


def add_image(request):
    form = ImageExtractionForm(request.POST or None, request.FILES or None)

    if request.method == "GET":
        return render(request, "add_image.html", {"form": form})
    if form.is_valid():
        form.save()
        new_picture = ImageExtraction.objects.last().user_image.url
        update_payload = {"picture": new_picture}
        user_id = request.session.get("user")["userinfo"]["sub"]
        api_url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {settings.AUTH0_TOKEN}",
            "Content-Type": "application/json",
        }
        response = requests.patch(
            api_url, headers=headers, data=json.dumps(update_payload)
        )
        if response.status_code == 200:
            request.session.get("user")["userinfo"]["picture"] = new_picture
        login(request)
        return redirect(reverse(index))
    return render(request, "add_image.html", {"form": form})
