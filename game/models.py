import uuid
from django.db import models
from card.models import Card

class Game(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_type = models.ForeignKey('Gametype', models.DO_NOTHING, blank=False, null=False)
    game_select_card_id = models.UUIDField(blank=False, null=True)
    game_all_select_card_id = models.JSONField(blank=False, null=True)  # JSON 형식으로 변경
    game_quest = models.TextField(blank=False, null=False)
    game_started_at = models.DateTimeField(blank=False, null=False)
    game_finished_at = models.DateTimeField(blank=False, null=True)

    class Meta:
        managed = True
        db_table = 'game'


class Gametype(models.Model):
    game_type_id = models.UUIDField(primary_key=True)
    game_type_all_card_num = models.IntegerField(blank=False, null=False)
    game_type_select_card_num = models.IntegerField(blank=False, null=False)
    game_type_fan_card_num = models.IntegerField(blank=False, null=False)
    game_type_name = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'gametype'