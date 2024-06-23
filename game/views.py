import uuid
from django.utils import timezone 
from rest_framework.decorators import api_view
from rest_framework import status
from config.utils import error_response, validate_serializer, exception_handler, success_response
from game.models import Gametype, Game, TaskStatus
from game.serializers import GameEndRequestSerializer, GameGetAnswerRequestSerializer, GameGetAnswerResponseSerializer
from game.serializers import GameRuleRequestSerializer, GameRuleResponseSerializer
from game.serializers import GameStartRequestSerializer, GameStartResponseSerializer
from game.serializers import GameSelectedCardInfoRequestSerializer, GameSelectedCardInfoResponseSerializer
from game.tasks import get_gemini_answer_task
from gemini.models import AIAnswer

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
    return success_response(response_data, status.HTTP_200_OK)


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

    return success_response(response_data, status.HTTP_200_OK)


@api_view(["POST"])
@exception_handler(view=True)
def game_end(request):
    """
    Get Answer of Horoscope
    """
    serializer = validate_serializer(GameEndRequestSerializer, request.data)

    game_id = serializer.get("game_id")
    print("game_id", game_id)
    select_card_id = serializer.get("select_card_id")
    # all_select_card_id = request.data.get("all_select_card_id")
    all_select_card_id = {}
    for key, value in serializer.get("all_select_card_id").items():
        all_select_card_id[key] = value

    game = Game.objects.get(game_id=game_id)
    task = get_gemini_answer_task.delay(game_id, select_card_id, all_select_card_id)
    TaskStatus.objects.create(task_status_id=task.id, task_status="READY", task_status_of_game=game)
    task_status = TaskStatus.objects.get(task_status_id=task.id)

    # if task_status.task_status == "READY":
    #     game_is_finished = False
    #     return success_response({"is_finished": game_is_finished}, status.HTTP_200_OK)
    
    # elif task_status.task_status == "STARTED":
    #     game_is_finished = False
    #     return error_response({"is_finished": game_is_finished}, status.HTTP_200_OK)
    
    # elif task_status.task_status == "FINISHED":
    #     game_is_finished = True
    #     return success_response({"is_finished": game_is_finished}, status.HTTP_200_OK)
    
    # else:
    #     return error_response({"is_finished": False}, status.HTTP_200_OK)
    return success_response({"task_id": task.id}, status.HTTP_200_OK)

# @api_view(["GET"])
@api_view(["POST"])
@exception_handler(view=True)
def task_status(request):
    serializer = validate_serializer(GameGetAnswerRequestSerializer, request.data)
    game_id = serializer.get("game_id")
    
    game = Game.objects.get(game_id=game_id)
    task_status = TaskStatus.objects.get(task_status_of_game=game)

    if task_status.task_status == "READY":
        return success_response({"success": "READY"}, status.HTTP_200_OK)
    
    elif task_status.task_status == "STARTED":
        return success_response({"success": "STARTED"}, status.HTTP_102_PROCESSING)
    
    elif task_status.task_status == "FINISHED":
        return success_response({"success": "FINISHED"}, status.HTTP_201_CREATED)


# @api_view(["GET"])
@api_view(["POST"])
@exception_handler(view=True)
def get_answer(request):
    """
    Get Gemini Answer
    """
    serializer = validate_serializer(GameGetAnswerRequestSerializer, request.data)
    game_id = serializer.get("game_id")
    game = Game.objects.get(game_id=game_id)
    print(game)

    response_data = AIAnswer.objects.get(ai_answer_of_game=game)
    ai_answer_path = response_data.ai_answer_path
    print(ai_answer_path)
    
    with open(ai_answer_path, "r") as file:
        response_data = file.read()

    return success_response({"answer": response_data}, status.HTTP_200_OK)
    


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

    return success_response(response_data, status.HTTP_200_OK)
