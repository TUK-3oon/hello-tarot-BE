from django.urls import path
from . import views

urlpatterns = [
    path("", views.google_ai, name="google_ai"),
]
