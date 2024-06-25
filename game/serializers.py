import json
from rest_framework import serializers
from game.models import Game, Gametype


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


class GameStartRequestSerializer(serializers.Serializer):
    game_type_id = serializers.UUIDField()


class GameStartResponseSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField()
    game_quest = serializers.CharField()
    class Meta:
        model = Game
        fields = ('game_id', 'game_quest')


class GameEndRequestSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()
    select_card_id = serializers.UUIDField()
    all_select_card_id = serializers.DictField(child=serializers.UUIDField())


# class GameEndResponseSerializer(serializers.Serializer):
#     is_finished = serializers.BooleanField(default=False)


# class GameEndResponseSerializer(serializers.Serializer):
#     success = serializers.BooleanField(default=False)
#     game_id = serializers.UUIDField()
#     select_card_id = serializers.UUIDField()
#     all_select_card_id = serializers.DictField()


class GameSelectedCardInfoRequestSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()
    

class GameSelectedCardInfoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    game_id = serializers.UUIDField()
    select_card_id = serializers.UUIDField()
    all_select_card_id = serializers.DictField()

    def get_info(_game_id):
        game = Game.objects.get(game_id=_game_id)
        return {
            'success': game.game_finished_at is not None,
            'gameId': game.game_id,
            'selectCardId': game.game_select_card_id,
            'allSelectCardId': json.loads(game.game_all_select_card_id)
        }
    

class GameGetAnswerRequestSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()


class GameGetAnswerResponseSerializer(serializers.Serializer):
    ai_answer_id = serializers.UUIDField()
    ai_answer_path = serializers.CharField()
    ai_answer_of_game = serializers.UUIDField()