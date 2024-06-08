from django.urls import path
from init.views import DBInitAPIView

urlpatterns = [
    path('table/', DBInitAPIView.as_view(), name='db_init'),
]