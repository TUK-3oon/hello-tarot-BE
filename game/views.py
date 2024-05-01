from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GameRuleSerializer, GameQuestSerializer
import uuid
from .models import Gametype, Game

@api_view(["POST"])
def game_rule_by_type_name(request):
    game_type_name = request.data.get("game_type_name")
    
    try:
        game_type = Gametype.objects.get(game_type_name=game_type_name)
        serializer = GameRuleSerializer(game_type)

        return Response(serializer.data)
    except Gametype.DoesNotExist:
        return Response({"error": "Invalid gameType"}, status=400)


@api_view(["POST"])
def game_start(request):
    game_type_id = request.data.get("game_type_id")

    try:
        games = Game.objects.filter(game_type_id=game_type_id)
        if not games.exists():
            return Response({"error": "No game found for the given gameType"}, status=400)
        
        game = games.first()
        serializer = GameQuestSerializer(game)
        return Response(serializer.data)
    except Game.DoesNotExist:
        return Response({"error": "Invalid gameType"}, status=400)



@api_view(["POST"])
def game_end(request):
    game_id = request.data.get("game_id")
    select_card_id = request.data.get("select_card_id")
    all_select_card_id = request.data.get("all_select_card_id")

    try:
        game = Game.objects.get(game_id=game_id)

        return Response({"success": True})
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=404)

