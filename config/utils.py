import json
import re
from rest_framework import serializers

# 리스트 핸들링 안될듯
def convert_keys_to_snake_case(data: dict) -> dict:
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    if isinstance(data, dict):
        return {camel_to_snake(key): convert_keys_to_snake_case(value) if isinstance(value, dict) else value for key, value in data.items()}
    return data


def validate_serializer(serializer_class: serializers, request_data: dict) -> dict:
    """
    Validate serializer using `serializer_class` and `request_data`

    Args:
        `serializer_class` (class): serializer class
        `request_data` (dict): request data
    
    Returns:
        `serializer` (class): serializer class
    """
    serializers = serializer_class(data=request_data)
    serializers.is_valid(raise_exception=True)
    
    return convert_keys_to_snake_case(request_data)


from functools import wraps
import traceback
from card.models import Card
from game.models import Game, Gametype
from gemini.models import AIAnswer
from rest_framework import status
from rest_framework.response import Response

# def exception_handler(celery: bool = False, view: bool = False): 로 하면 분기처리 가능
def exception_handler(view: bool = False):
    def exception_handler_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Card.DoesNotExist as e:
                print(f"An error occurred in {func.__name__}: {e}")
                return error_response("Invalid Card", status.HTTP_404_NOT_FOUND)
            except Game.DoesNotExist as e:
                print(f"An error occuerd in {func.__name__}: {e}")
                return error_response("Invalid Game", status.HTTP_404_NOT_FOUND)
            except Gametype.DoesNotExist as e:
                print(f"An error occurred in {func.__name__}: {e}")
                return error_response("Invalid Game Type", status.HTTP_404_NOT_FOUND)
            # except AIAnswer.DoesNotExist as e:
            #     print(f"An error occurred in {func.__name__}: {e}")
            #     return error_response("Invalid AI Answer", status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"An error occurred in {func.__name__}: {e}")
                print(e)
                return error_response("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return wrapper
    return exception_handler_decorator


def error_response(error: str, status_code: int):
    return Response({"error": error}, status_code)
    

def success_response(data, status_code: int):
    return Response({"data": data}, status=status_code)


def get_text_answer(response_text):
    """
    Get Answer from Gemini AI
    """
    candidates = response_text.candidates if response_text else []

    text = []
    for candidate in candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                text.append(part.text)

    response_data = text

    if isinstance(response_data, dict):
        response = json.dumps(response_data, ensure_ascii=False)
        return response
    return response_data

def remove_special_characters(text: str):
    """
    To remove '*', '\\', '\n' in text.
    """
    text = text.replace("\\", "")
    text = text.replace("\n", "")
    text = text.replace("*", "")
    # text = text.replace("n", "")
    
    return text


def get_content(response_text):
    """
    Get Content from Gemini AI
    """
        # candidates 리스트에서 text 추출
    if "result" in response_text and "candidates" in response_text["result"]:
        candidates = response_text["result"]["candidates"]
        for candidate in candidates:
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                for part in parts:
                    if "text" in part:
                        extracted_text = part["text"]
                        return extracted_text