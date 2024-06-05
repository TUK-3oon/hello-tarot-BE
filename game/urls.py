from django.urls import path
from . import views

urlpatterns = [
    path("rule/", views.game_rule_by_type_name, name="game_rule_by_type"),
    path("start/", views.game_start, name="game_start"),
    path("end/", views.game_end, name="game_end"),
    path("end/info/", views.select_card_info, name="select_card_info"),
]
