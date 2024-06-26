from django.urls import path
from game import views

urlpatterns = [
    path("rule/", views.game_rule_by_type_name, name="game_rule_by_type"),
    path("start/", views.game_start, name="game_start"),
    path("end/", views.game_end, name="game_end"),
    path("end/info/", views.select_card_info, name="select_card_info"),
    path("answer/", views.get_answer, name="get_gemini_answer"),
    path("status/", views.task_status, name="get_task_status"),
]
