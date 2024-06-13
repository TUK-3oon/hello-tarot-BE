from rest_framework import serializers
from card.models import Card

class CardBackImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('card_image_url',)


class CardFrontInfoSerializer(serializers.ModelSerializer):
    card_contents = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ("card_id", "card_name", "card_number", "card_image_url", "card_contents")

    def get_card_contents(self, obj):
        return {
            'forward': obj.card_forward,
            'reverse': obj.card_reverse
        }
    
class HoroscopeRequestSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    card_id = serializers.UUIDField()


class HoroscopeResponseSerializer(serializers.ModelSerializer):
    forward = serializers.CharField(source='card_forward')
    reverse = serializers.CharField(source='card_reverse')

    class Meta:
        model = Card
        fields = ('forward', 'reverse')


class AnswerRequestSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()


class AnswerResponseSerializer(serializers.Serializer):
    forward = serializers.CharField(source='card_forward')
    reverse = serializers.CharField(source='card_reverse')

    class Meta:
        model = Card
        fields = ('forward', 'reverse')