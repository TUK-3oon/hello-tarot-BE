import uuid
from django.db import models

from game.models import Game

class AIAnswer(models.Model):
    """
    AI Answer Model
    """
    ai_answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ai_answer = models.TextField(blank=True, null=False)
    ai_answer_created_at = models.DateTimeField(auto_now_add=True)
    ai_answer_of_game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'ai_answer'