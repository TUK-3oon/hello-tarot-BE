import json
from django.shortcuts import get_object_or_404
from card.models import Card
from config import settings
from config.utils import get_text_answer, validate_serializer, exception_handler, success_response
from game.models import Game
from gemini.models import AIAnswer
from gemini.serializer import GoogleAIRequestSerializer
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone

GOOGLE_API_KEY = settings.GOOGLE_API_KEY

@api_view(["POST"])
@exception_handler(view=True)
def google_ai(request):
    """
    Use Gemini Prompt View

    Request:
        {
            "game_id": uuid of game,
            "select_card_id": selected card id from user
        }

    Response:
        {
            "response": [
                {
                    "forward": [
                        ...
                    ],
                    "reverse": [
                        ...
                    ]
                }
            ]
        }
    """
    serializer = validate_serializer(GoogleAIRequestSerializer, request.data)

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    game_id = serializer.get('game_id')
    select_card_id = serializer.get('select_card_id')

    game = Game.objects.get(pk=game_id)
    game_type_name = game.game_type
    game_question = game.game_quest

    card = Card.objects.get(pk=select_card_id)
    card_image_url = card.card_image_url

    content = f"""
    타로 게임을 시작할거야. 너는 세계에서 알아주는 타로술사야. 이번 게임의 주제는 '{game_type_name}'야.
    너가 고객에게 한 질문은 '{game_question}'야.
    고객이 고른 카드의 그림은 '{card_image_url}'야.
    이 3가지의 내용을 조합해 적절한 운세 답변을 내줘.
    긍정적인 답변과 부정적인 답변으로 나누어서 답변해주고, 각각의 상황에 앞으로 어떻게 행동하면 좋을지도 알려줘.
    답변의 형식은 JSON이고, 긍정적인 답변의 키는 'forward', 부정적인 답변의 키는 'reverse'로 표시해줘.
    하나의 key에 해당하는 값들은 리스트로 묶어서 표시하고, 무분별한 줄바꿈은 하지말고, 답변은 이쁘게 출력해.
    그리고 답변은 코드 블럭으로 감싸지말고 JSON 형식에 맞게 출력해.
    코드 블럭으로 절대 감싸지마.
    """

    response_text = model.generate_content(content)
    candidates = response_text.candidates if response_text else []

    response_data = get_text_answer(candidates)

    AIAnswer.objects.create(
        ai_answer=response_data,
        ai_answer_created_at=timezone.now(),
        ai_answer_of_game=game 
    )

    return success_response(json.dumps(response_data, ensure_ascii=False, indent=4), status.HTTP_200_OK)
    # return success_response(response_data, status.HTTP_200_OK)