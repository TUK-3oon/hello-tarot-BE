from rest_framework import serializers
from .models import Game, Gametype

class GameRuleRequestSerializer(serializers.Serializer):
    game_type_name = serializers.CharField()


class GameRuleResponseSerializer(serializers.ModelSerializer):
    game_type_id = serializers.UUIDField()
    game_type_name = serializers.CharField()
    game_info = serializers.SerializerMethodField()

    class Meta:
        model = Gametype
        fields = ('game_type_id', 'game_type_name', 'game_info')

    def get_game_info(self, obj):
        return {
            'allCardNum': obj.game_type_all_card_num,
            'selectCardNum': obj.game_type_select_card_num,
            'fanCardNum': obj.game_type_fan_card_num
        }


class GameQuestRequestSerializer(serializers.Serializer):
    game_type_id = serializers.UUIDField()


class GameQuestResponseSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField()
    game_quest = serializers.CharField()
    class Meta:
        model = Game
        fields = ('game_id', 'game_quest')



"""
    Get Answer of Horoscope
     
    Args:
        request: {
            game_id(uuid): Id of Game
            game_select_card_id(uuid): Select Card Id by Client
            game_all_select_card_id: {
                game_select_card_id(uuid): Selected card Id in Game
                game_select_card_id(uuid): Selected card Id in Game
                game_select_card_id(uuid): Selected card Id in Game
            }
        }
    Returns:
        response : {
            success(boolean): True
        }
    """
class GameEndRequestSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()
    select_card_id = serializers.UUIDField()
    all_select_card_id = serializers.DictField(child=serializers.UUIDField())
