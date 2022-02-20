from django.urls import path

from . import views

app_name = "gw2inv_app"

urlpatterns = [
    path("", views.index),
    path("full_update", views.full_update, name="full_update"),
]
