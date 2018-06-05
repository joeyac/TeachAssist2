from rest_framework import serializers


class RequirementCreateSerializer(serializers.Serializer):
    prefer = serializers.BooleanField()

