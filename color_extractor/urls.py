from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("images/", views.images, name="images"),
    path("delete_image/<int:image_id>/", views.delete_image, name="delete_image"),
]
