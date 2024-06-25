import json
import os
import uuid
from celery import shared_task
from django.utils import timezone
from card.models import Card
from config.settings import GOOGLE_API_KEY
from game.models import Game, TaskStatus
from gemini.models import AIAnswer
import google.generativeai as genai

@shared_task(bind=True)
def get_gemini_answer_task(self, game_id, select_card_id, all_select_card_id):
    """
    Get Gemini Answer
    """
    task_id = self.request.id

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    game = Game.objects.get(game_id=game_id)

    card = Card.objects.get(pk=select_card_id)
    task_status, created = TaskStatus.objects.get_or_create(
        task_status_id=task_id, 
        defaults={'task_status_of_game': game, 'task_status': 'READY'}
    )

    content = f"""
    타로 게임을 시작할거야. 너는 세계에서 알아주는 타로술사야. 이번 게임의 주제는 '{game.game_type}'야.
    타로술사가 사용자에게 질문한 내용은 '{game.game_quest}'야.
    고객이 고른 카드의 그림은 '{card.card_image_url}'야.
    이 3가지의 내용을 조합해 적절한 운세 답변을 1000자 내외로 작성해줘.
    답변에 포함될 내용은 다음과 같아.
    
    1. 카드의 대표적인 의미
    2. 카드의 이미지 
    3. 질문에 대한 답변
    4. 긍정적인 답변
    5. 부정적인 답변
    6. 각각의 상황에 따른 행동 방향 
    7. 카드의 그림을 분석하고, 그림에 들어가있는 각각의 요소가 각각의 상황일 때 무엇을 의미하는지
    
    위의 주제에 대한 답변을 작성하고, 위에 적힌 키워드들을 포함해서 답변할 필요는 없어.
    답변은 TEXT 형식이야.
    답변을 작성할 때 "어떤 답변: 내용" 형식으로 대답하지 말고, 답변 내용만 작성해.
    너는 타로술사지만, 답변을 내줄 때는 존댓말로 대답해.
    
    항상 답변의 처음에는 '~ 카드를 선택하셨습니다.'라는 문구를 넣어.
    예를 들어 만약 사용자가 '마술사 카드'를 선택했다면, '당신은 마술사 카드를 선택하셨습니다.'라는 문구를 넣으면 돼.
    답변의 마지막에는 항상 사용자가 선택한 카드의 요소에 대한 설명을 작성해.
    예를 들면 '마지막으로, 카드의 그림에 대한 설명을 드리겠습니다. 이 카드에는 ~가 그려져 있습니다. 이 그림은 ~를 의미합니다.' 이런 식으로 작성해.
    """
    
    task_status.task_status = "STARTED"
    task_status.save()
    
    response_from_gemini = model.generate_content(content)


    data_files_dir = "data/files"
    os.makedirs(data_files_dir, exist_ok=True)
    file_path = os.path.join(data_files_dir, f"{task_id}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response_from_gemini.text)

    AIAnswer.objects.create(
        ai_answer_id=uuid.uuid4(),
        ai_answer_path=file_path,
        ai_answer_created_at=timezone.now(),
        ai_answer_of_game=game 
    )

    game_finish_options = {
        'game_id': game_id,
        'game_select_card_id': select_card_id,
        'game_all_select_card_id': json.dumps(all_select_card_id),
        'game_finished_at': timezone.now(),
        'game_is_finished': True
    }
    Game.finished_game(**game_finish_options)

    task_status.task_status = "FINISHED"
    task_status.save()
