from .models import Card
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CardBackImgSerializer, CardFrontInfoSerializer, HoroscopeRequestSerializer, HoroscopeResponseSerializer

@api_view(["GET"])
def get_card_back_image(request):

    cards = Card.objects.all().values() 

    serializer = CardBackImgSerializer(cards, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_card_front_info(request):

    cards = Card.objects.all()

    serializer = CardFrontInfoSerializer(cards, many=True)

    return Response(serializer.data) 


@api_view(["POST"])
def get_answer(request):

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
