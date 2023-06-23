from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse

from color_extractor.forms import ImageExtractionForm, SignUpForm, LoginForm
from color_extractor.models import ImageExtraction
from color_extractor.tokens import account_activation_token


def index(request):
    context = {
        "msg": "Home page",
        "user": request.user,
    }
    return render(request, "index.html", context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string(
                "account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": user.pk,
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user("Підтвердьте реєстрацію", message)
            return redirect("account_activation_sent")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def account_activation_sent(request):
    message = "Please confirm your email address to complete the registration."
    return render(request, "account_activation_sent.html", {"message": message})


def activate(request, uidb64, token):
    try:
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("home")
    else:
        return render(request, "account_activation_invalid.html")


def account_activation_invalid(request):
    message = "Account activation invalid."
    return render(request, "account_activation_invalid.html", {"message": message})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("home")
            else:
                usernames = User.objects.values_list("username", flat=True)
                if username in usernames:
                    msg = "Невірний пароль або ви не підтвердили реєстрацію на пошті"
                else:
                    msg = "Спочатку зареєструйтесь будь ласка"
                return HttpResponse(msg)
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def images(request):
    images_list = ImageExtraction.objects.all().order_by("-id")
    return render(request, "images.html", {"images_list": images_list})


def add_image(request):
    form = ImageExtractionForm(request.POST or None, request.FILES or None)

    if request.method == "GET":
        return render(request, "add_image.html", {"form": form})
    if form.is_valid():
        form.save()
        return redirect(reverse(images))
    return render(request, "add_image.html", {"form": form})
