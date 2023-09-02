from io import BytesIO
from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.core.files import File
from django.shortcuts import redirect, render
from django.urls import reverse

from color_extractor.forms import ImageExtractionForm
from color_extractor.models import ImageExtraction
from color_extractor.services import extract_colors


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
    return render(request, "index.html")


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("images")))


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
    s = request.session.get("user")
    if s:
        sub = s["userinfo"]["sub"]
        user_email = s["userinfo"]["email"]

    if request.method == "POST":
        form = ImageExtractionForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data["user_image"].read()

            instance = form.save(commit=False)
            instance.user_email = user_email
            instance.image_name = sub
            instance.save()

            result_image_data = extract_colors(uploaded_image)
            image_extraction = ImageExtraction(
                user_email=user_email,
                image_name=sub,
            )
            result_image_file = File(BytesIO(result_image_data))
            image_extraction.user_image.save("result.png", result_image_file)
            image_extraction.save()
            return redirect(reverse("images"))
    else:
        form = ImageExtractionForm()

    images_list = []
    if s:
        images_list = ImageExtraction.objects.filter(image_name=sub).order_by("-id")

    return render(
        request,
        "images.html",
        context={
            "session": s,
            "images_list": images_list,
            "form": form,
        },
    )
