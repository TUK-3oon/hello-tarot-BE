from rest_framework import serializers
from .models import Game, Gametype

class GameRuleSerializer(serializers.ModelSerializer):
    game_type_id = serializers.UUIDField(source='game_type_id')
    game_type_name = serializers.CharField(source='game_type_name')
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



class GameQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_quest', 'game_id',]