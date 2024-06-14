from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.utils import validate_serializer, exception_handler, success_response
from game.models import Game
from card.models import Card
from card.serializers import AnswerResponseSerializer, CardBackImgSerializer, CardFrontInfoSerializer, HoroscopeRequestSerializer, HoroscopeResponseSerializer, AnswerRequestSerializer


@api_view(["GET"])
@exception_handler(view=True)
def get_card_back_image(request):
    """
    Get Card Back images
     
    Args:\n
        request: {
            None
            }


    Returns:\n
        reponse: {    
            image(str) : image url 
        }
    """
    cards = Card.objects.all()
    response_data = CardBackImgSerializer(instance=cards, many=True).data

    return success_response(response_data, status.HTTP_200_OK)


@api_view(["GET"])
@exception_handler(view=True)
def get_card_front_info(request):
    """
    Get Card Front Informations
     
    Args:\n
        request: {
            None
        }


    Returns:\n
        response: {
            card_id(uuid) : Primary key value of Card
            card_name(str) : Name of Card
            card_number(int) : Index of Card
            card_image_url(str) : Image URL of Card's front 
            card_contents : { 
                forward(str) : Positive Content
                reverse(str) : Negative Content
            }
        }
    """
    cards = Card.objects.all()
    response_data = CardFrontInfoSerializer(cards, many=True).data

    return success_response(response_data, status.HTTP_200_OK)


@api_view(["POST"])
@exception_handler(view=True)
def get_answer_horoscope(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            date(datetime): DateTime of Today
            card_id(uuid): Id of Card
        }


    Returns:\n
        response : {
            forward(str) : Positive Content
            reverse(str) : Negative Content
        }
    """
    serializer = validate_serializer(HoroscopeRequestSerializer, request.data)

    card_id = serializer.get('card_id')
    card = Card.objects.get(card_id=card_id)
    response_data = HoroscopeResponseSerializer(card).data
    
    return success_response(response_data, status.HTTP_200_OK)
    

@api_view(["POST"])
@exception_handler(view=True)
def get_answer(request):
    """
    Get Answer of Horoscope
     
    Args:\n
        request: {
            game_id(uuid): Id of Game
        }


    Returns:\n
        response : {
            forward(str) : Positive Content
            reverse(str) : Negative Content
        }
    """
    serializer = validate_serializer(AnswerRequestSerializer, request.data)

    game_id = serializer.get('game_id')
    game = Game.objects.get(game_id=game_id)

    response_data = AnswerResponseSerializer(game).data
    
    return success_response(response_data, status.HTTP_200_OK)