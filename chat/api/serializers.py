from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, max_length=400)
    code = serializers.BooleanField(required=False)