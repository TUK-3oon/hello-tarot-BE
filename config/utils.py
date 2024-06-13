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
                return error_response("Invalid Card", status.HTTP_400_BAD_REQUEST)
            except Game.DoesNotExist as e:
                print(f"An error occuerd in {func.__name__}: {e}")
                return error_response("Invalid Game", status.HTTP_400_BAD_REQUEST)
            except Gametype.DoesNotExist as e:
                print(f"An error occurred in {func.__name__}: {e}")
                return error_response("Invalid Game Type", status.HTTP_400_BAD_REQUEST)
            except AIAnswer.DoesNotExist as e:
                print(f"An error occurred in {func.__name__}: {e}")
                return error_response("Invalid AI Answer", status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"An error occurred in {func.__name__}: {e}")
                return error_response("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return wrapper
    return exception_handler_decorator


def error_response(error: str, status_code: int):
    return Response({"error": error}, status_code)
    
def success_response(data: dict, status_code: int):
    return Response(data, status=status_code)