from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.signup, name="signup"),
    path(
        "account_activation_sent/",
        views.account_activation_sent,
        name="account_activation_sent",
    ),
    path(
        "account_activation_invalid/",
        views.account_activation_invalid,
        name="account_activation_invalid",
    ),
    path(
        "activate/<uidb64>/<token>/",
        views.activate,
        name="activate",
    ),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("add_image/", views.add_image, name="add_image_view"),
    path("images/", views.images, name="images"),
]
