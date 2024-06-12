import json
import uuid
from django.utils import timezone 
from rest_framework.decorators import api_view
from rest_framework import status
from config.utils import validate_serializer, exception_handler, success_response
from game.models import Gametype, Game
from game.serializers import GameEndResponseSerializer, GameEndRequestSerializer
from game.serializers import GameRuleRequestSerializer, GameRuleResponseSerializer
from game.serializers import GameStartRequestSerializer, GameStartResponseSerializer
from game.serializers import GameSelectedCardInfoRequestSerializer, GameSelectedCardInfoResponseSerializer

@api_view(["POST"])
@exception_handler(view=True)
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
                game_type_all_card_num(int): All of Card Numbers in Game Type - 52
                game_type_select_card_num(int): Selected Card Numbers in Game Type - 1
                game_type_fan_card_num(int): Fanned Card Number in Game Type - 3
            }
        }
    """
    serializer = validate_serializer(GameRuleRequestSerializer, request.data)
    game_type_name = serializer.get("game_type_name")

    game_type = Gametype.objects.get(game_type_name=game_type_name)
    response_data = GameRuleResponseSerializer(game_type).data
    return success_response(response_data, status_code=status.HTTP_200_OK)


@api_view(["POST"])
@exception_handler(view=True)
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
    serializer = validate_serializer(GameStartRequestSerializer, request.data)
    game_type_id = serializer.get("game_type_id")
    game_type = Gametype.objects.get(game_type_id=game_type_id)

    game_crate_options = {
        'game_id': uuid.uuid4(),
        'game_type': game_type,
        'game_started_at': timezone.now(),
        'game_quest': "가장 고르고싶은 카드를 선택해주세요."
    }
    game = Game.objects.create(**game_crate_options)
    response_data = GameStartResponseSerializer(game).data

    return success_response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@exception_handler(view=True)
def game_end(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            game_id(uuid): Id of Game
            select_card_id(uuid): Select Card Id by Client
            all_select_card_id: {  
                "primary_select_card_id_1": Selected card Id in Game (uuid)
                "sceondary_select_card_id": Selected card Id in Game (uuid)
                "tertiary_select_card_id": Selected card Id in Game (uuid)
            }
        }

    Returns:\n
        response : {
            success(boolean): True
        }
    """
    serializer = validate_serializer(GameEndRequestSerializer, request.data)
    game_id = serializer.get("game_id")
    select_card_id = serializer.get("select_card_id")
    all_select_card_id = {}

    for key, value in request.data.get("all_select_card_id").items():
        all_select_card_id[key] = value

    response_data = GameEndResponseSerializer(serializer).data
    response_data["success"] = True

    game_crate_options = {
        'game_id': game_id,
        'select_card_id': select_card_id,
        'all_select_card_id': json.dumps(all_select_card_id),
        'finished_at': timezone.now()
    }
    Game.finished_game(**game_crate_options)

    return success_response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@exception_handler(view=True)
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
    serializer = validate_serializer(GameSelectedCardInfoRequestSerializer, request.data)
    game_id = serializer.get("game_id")
    response_data = GameSelectedCardInfoResponseSerializer.get_info(_game_id=game_id)

    return success_response(response_data, status=status.HTTP_200_OK)
