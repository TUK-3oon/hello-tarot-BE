from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GameRuleRequestSerializer, GameRuleResponseSerializer
from .serializers import GameQuestRequestSerializer, GameQuestResponseSerializer
from .serializers import GameEndRequestSerializer
import uuid
from rest_framework import status
from .models import Gametype, Game


@api_view(["POST"])
def game_rule_by_type_name(request):
    """
    Post Game Rule By Game Type Name

    Args:\n
        request: {
            game_type_name(str): Name of Game Type
        }


    Returns:\n
        response : {
            game_type_id(uuid):
            game_type_name(str):
            game_info: {
                game_type_all_card_num(int): All of Card Numbers in Game Type
                game_type_select_card_num(int): Selected Card Numbers in Game Type
                game_type_fan_card_num(int): Fanned Card Number in Game Type
            }
        }
    """
    serializer = GameRuleRequestSerializer(data=request.data)

    if serializer.is_valid():
        game_type_name = serializer.validated_data.get("game_type_name")
    
        try:
            game_type_name = Gametype.objects.get(game_type_name=game_type_name)
            
        except Gametype.DoesNotExist:
            return Response({"error": "Invalid gameType"}, status=400)

        response_serializer = GameRuleResponseSerializer(game_type_name)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    return Response(response_serializer.data, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def game_start(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            game_type_id(uuid): Id of Game Type
        }


    Returns:\n
        response : {
            game_id(uuid): Id of Game 
            game_question: Question of Game
        }
    """
    serializer = GameQuestRequestSerializer(data=request.data)
    if serializer.is_valid():
        game_type_id = serializer.validated_data.get("game_type_id")

        try:
            games = Game.objects.filter(game_type_id=game_type_id)
            game = games.first()
        except Game.DoesNotExist:
            return Response({"error": "Invalid gameType"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_serializer = GameQuestResponseSerializer(game)
            
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def game_end(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            game_id(uuid): Id of Game
            select_card_id(uuid): Select Card Id by Client
            all_select_card_id: {
                select_card_id(uuid): Selected card Id in Game
                select_card_id(uuid): Selected card Id in Game
                select_card_id(uuid): Selected card Id in Game
            }
        }


    Returns:\n
        response : {
            success(boolean): True
        }
    """
    serializer = GameEndRequestSerializer(data=request.data)
    if serializer.is_valid():
        game_id = serializer.validated_data.get("game_id")
        select_card_id = serializer.validated_data.get("select_card_id")
        all_select_card_id = serializer.validated_data.get("all_select_card_id")

        try:
            game = Game.objects.get(game_id=game_id)
            game.game_select_card_id = select_card_id
            game.game_all_select_card_id = all_select_card_id
            game.save()

            return Response({"success": True}, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
