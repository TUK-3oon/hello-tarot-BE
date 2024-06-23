# from rest_framework import serializers


# class PartSerializer(serializers.Serializer):
#     text = serializers.CharField()


# class ContentSerializer(serializers.Serializer):
#     parts = PartSerializer(many=True)


# class GoogleAIRequestSerializer(serializers.Serializer):
#     select_card_id = serializers.UUIDField()
#     game_id = serializers.UUIDField()


# class GoogleAIResponseSerializer(serializers.Serializer):
#     # response = serializers.ListField(child=serializers.CharField())
#     response = serializers.CharField()
