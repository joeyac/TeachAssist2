from rest_framework import serializers
from utils.constants import UserType
from course_arrangement.models import *


class RequirementCreateSerializer(serializers.Serializer):
    favorite = serializers.IntegerField(min_value=-10, max_value=5)
    lecture_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

    def validate(self, data):
        if data['favorite'] not in RequireDegree.choices():
            raise serializers.ValidationError("favorite should in {}".format(RequireDegree.model_choices()))

        lecture = Requirement.objects.filter(id=data['lecture_id']).first()
        if not lecture:
            raise serializers.ValidationError("lecture ({}) does not exist.".format(data['lecture_id']))

        teacher = User.objects.filter(id=data['teacher_id'], user_type=UserType.TEACHER).first()
        if not teacher:
            raise serializers.ValidationError("teacher ({}) does not exist.".format(data['teacher_id']))

        return data

