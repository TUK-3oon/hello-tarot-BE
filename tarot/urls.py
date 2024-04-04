from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("gameInfo/", views.my_view, name="game_info"),
]
