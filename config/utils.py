import re
from rest_framework import serializers
from functools import wraps
from card.models import Card
from game.models import Game, Gametype
from rest_framework import status
from rest_framework.response import Response


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


def load_content_template(template_path, context):
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    return template.format(**context)