from django.urls import path
from init.views import init_db

urlpatterns = [
    path('table/', init_db, name='db_init'),
]