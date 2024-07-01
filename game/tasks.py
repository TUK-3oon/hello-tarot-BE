import json
import os
from pathlib import Path
import uuid
from celery import shared_task
from django.utils import timezone
from card.models import Card
from config.settings import GOOGLE_API_KEY
from config.utils import load_content_template
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
    task_status = TaskStatus.objects.get(task_status_id=task_id)

    context = {
        'game_type': game.game_type,
        'game_quest': game.game_quest,
        'card_image_url': card.card_image_url
    }

    template_path = Path("game/templates/static/content.txt")
    content = load_content_template(template_path, context)
    
    if content:
        task_status.task_status = "STARTED"
        task_status.save()
    
        response_from_gemini = model.generate_content(content)


        data_files_dir = Path("data/files")
        data_files_dir.mkdir(parents=True, exist_ok=True)
        file_path = data_files_dir / f"{task_id}.txt"

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
