from django.urls import path

from . import views


urlpatterns = [
    path("stats/", views.stats, name="stats"),
    path("register/", views.register, name="register"),
]