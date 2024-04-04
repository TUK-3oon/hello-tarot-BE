import json
import pprint

from django.http import JsonResponse
from .models import Card, Game, Gametype


def my_view(request):

    cards = Card.objects.all().values()

    games = Game.objects.all().values()

    gametype = Gametype.objects.all().values()

    context = {
        'cards': list(cards),
        'games': list(games),
        'gametypes': list(gametype),
    }

    pprint.pprint(context)

    return JsonResponse(context)
