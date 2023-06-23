from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.signup),
    path(
        "activate/<uidb64>/<token>/",
        views.activate,
        name="activate",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("add_image/", views.add_image, name="add_image_view"),
    path("images/", views.images, name="images"),
]
