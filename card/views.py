from game.models import Game
from .models import Card
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AnswerResponseSerializer, CardBackImgSerializer, CardFrontInfoSerializer, HoroscopeRequestSerializer, HoroscopeResponseSerializer, AnswerRequestSerializer

@api_view(["GET"])
def get_card_back_image(request):
    """
    Get Card Back images
     
    Args:
        request: {
            None
            }
    Returns:
        reponse: {    
            image(str) : image url 
        }
    """

    cards = Card.objects.all().values() 

    serializer = CardBackImgSerializer(cards, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_card_front_info(request):
    """
    Get Card Front Informations
     
    Args:
        request: {
            None
        }
    Returns:
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

    serializer = CardFrontInfoSerializer(cards, many=True)

    return Response(serializer.data) 


@api_view(["POST"])
def get_answer_horoscope(request):
    """
    Get Answer of Horoscope
     
    Args:
        request: {
            date(datetime): DateTime of Today
            card_id(uuid): Id of Card
        }
    Returns:
        response : {
            forward(str) : Positive Content
            reverse(str) : Negative Content
        }
    """

    serializer = HoroscopeRequestSerializer(data=request.data)

    if serializer.is_valid():
        card_id = serializer.validated_data.get('card_id')
        date = serializer.validated_data.get('date')

        try:
            card = Card.objects.get(card_id=card_id)
        except Card.DoesNotExist:
            return Response({"error": "Card not found."}, status=status.HTTP_404_NOT_FOUND)

        response_serializer = HoroscopeResponseSerializer(card)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_answer(request):
    """
    Get Answer of Horoscope
     
    Args:
        request: {
            game_id(uuid): Id of Game
        }
    Returns:
        response : {
            forward(str) : Positive Content
            reverse(str) : Negative Content
        }
    """

    serializer = AnswerRequestSerializer(data=request.data)

    if serializer.is_valid():
        game_id = serializer.validated_data.get('game_id')

        try:
            game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({"error": "Card not found."}, status=status.HTTP_404_NOT_FOUND)

        response_serializer = AnswerResponseSerializer(game)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)