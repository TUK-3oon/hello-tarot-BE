from rest_framework import serializers


class PartSerializer(serializers.Serializer):
    text = serializers.CharField()


class ContentSerializer(serializers.Serializer):
    parts = PartSerializer(many=True)


class GoogleAIRequestSerializer(serializers.Serializer):
    contents = ContentSerializer(many=True)


class GoogleAIResponseSerializer(serializers.Serializer):
    response = serializers.ListField(child=serializers.CharField())
