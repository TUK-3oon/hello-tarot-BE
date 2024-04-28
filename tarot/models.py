from django.db import models

class Card(models.Model):
    card_id = models.UUIDField(primary_key=True)
    card_name = models.TextField(blank=False, null=False)
    card_number = models.IntegerField(blank=False, null=False)
    card_image_url = models.TextField(blank=False, null=False)
    card_forward = models.TextField(blank=False, null=False)
    card_reverse = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'card'
        

class Game(models.Model):
    game_id = models.UUIDField(primary_key=True)
    game_type = models.ForeignKey('Gametype', models.DO_NOTHING, blank=False, null=False)
    game_select_card_id = models.IntegerField(blank=False, null=False)
    game_all_select_card_id = models.IntegerField(blank=False, null=False)
    game_quest = models.TextField(blank=False, null=False)
    game_started_at = models.DateTimeField(blank=False, null=False)
    game_finished_at = models.DateTimeField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'game'


class Gametype(models.Model):
    game_type_id = models.UUIDField(primary_key=True)
    game_type_all_card_num = models.IntegerField(blank=False, null=False)
    game_type_select_card_num = models.IntegerField(blank=False, null=False)
    game_type_fan_card_num = models.IntegerField(blank=False, null=False)
    game_type = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'gametype'
