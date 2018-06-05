from rest_framework import serializers


class SuccessResponseSerializer(serializers.Serializer):
    error = serializers.CharField(default="", allow_blank=True)
    data = serializers.CharField(default="data")


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(default="error")
    data = serializers.CharField(default="msg")
