from rest_framework import serializers
from .models import ConfigRequest, StatusMessage

class ConfigSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    target = serializers.CharField(max_length=255)
    config = serializers.CharField()

    def create(self, validated_data):
        """
        Create a config object
        """
        return ConfigRequest.objects.create(**validated_data)

class StatusMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    response = serializers.CharField
    status = serializers.CharField(max_length=255)
