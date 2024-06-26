from django.urls import path
from card import views

urlpatterns = [
    path("back/", views.get_card_back_image, name="card_back"),
    path("front/all/", views.get_card_front_info, name="card_front_all"),
    path("answer/horoscope/", views.get_answer_horoscope, name="get_answer_horoscope"),
    path("answer/", views.get_answer, name="get_answer"),
]
