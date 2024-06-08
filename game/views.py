import json
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from game.models import Gametype, Game
from game.serializers import GameSelectedCardInfoSerializer
from game.serializers import GameRuleRequestSerializer, GameRuleResponseSerializer
from game.serializers import GameQuestRequestSerializer, GameQuestResponseSerializer
from game.serializers import GameEndRequestSerializer
from django.utils import timezone 


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
            game_type = Gametype.objects.get(game_type_name=game_type_name)
        except Gametype.DoesNotExist:
            return Response({"error": "Invalid gameType"}, status=400)

        response_serializer = GameRuleResponseSerializer(game_type)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    return Response(response_serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def game_start(request):
    """
    게임을 시작합니다.
     
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
            game_type = Gametype.objects.get(game_type_id=game_type_id)
        except Gametype.DoesNotExist:
            return Response({"error": "Invalid gameType"}, status=status.HTTP_400_BAD_REQUEST)
        
        game = Game.objects.create(
            game_id=uuid.uuid4(),
            game_type=game_type,
            game_started_at=timezone.now(),
            game_quest="질문입니다."  # 실제 질문 텍스트로 변경
        )
        
        response_data = {
            "game_id": game.game_id,
            "game_question": game.game_quest
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def game_end(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            game_id(uuid): Id of Game
            select_card_id(uuid): Select Card Id by Client
            all_select_card_id: {  # Dictionary containing selected card IDs
                "select_card_id_1": Selected card Id in Game (uuid)
                "select_card_id_2": Selected card Id in Game (uuid)
                "select_card_id_3": Selected card Id in Game (uuid)
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
        all_select_card_id = {}  # Empty list to store extracted card IDs

        # Extract card IDs from the dictionary
        for key, value in request.data.get("all_select_card_id").items():
            all_select_card_id[key] = value

        try:
            game = Game.objects.get(game_id=game_id)
            game.game_select_card_id = select_card_id
            game.game_all_select_card_id = json.dumps(all_select_card_id)  # Convert list to JSON string
            # Set the end time to the current time
            game.game_finished_at = timezone.now()
            game.save()

            response_data = {
                "success": True,
                "game_id": game_id,
                "select_card_id": select_card_id,
                "all_select_card_id": all_select_card_id
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def select_card_info(request):
    """
    Get Card Info
     
    Args:\n
        request: {
            game_id(uuid): Id of Game
        }

    Returns:\n
        response : {
            success(Boolean): Status Game End
            game_id(uuid): Id of Game
            all_select_card_id: {  # Dictionary containing selected card IDs
                "select_card_id_1": Selected card Id in Game (uuid)
                "select_card_id_2": Selected card Id in Game (uuid)
                "select_card_id_3": Selected card Id in Game (uuid)
            }
        }
    """
    serializer = GameSelectedCardInfoSerializer(data=request.data)
    if serializer.is_valid():
        game_id = serializer.validated_data.get("game_id")
        all_select_card_id = Game.objects.get(game_id=game_id).game_all_select_card_id

        try:
            response_data = {
                "success": True,
                "game_id": game_id,
                "all_select_card_id": json.loads(all_select_card_id)
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)