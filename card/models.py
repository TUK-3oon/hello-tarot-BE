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