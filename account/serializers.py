from rest_framework import serializers
from utils.constants import UserType


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
    email = serializers.EmailField(max_length=64)
    user_type = serializers.ChoiceField(choices=UserType.model_choices(), default=UserType.STUDENT)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
