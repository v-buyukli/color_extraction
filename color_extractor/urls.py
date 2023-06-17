from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add_image/", views.add_image, name="add_image_view"),
    path("images/", views.images, name="images"),

]
