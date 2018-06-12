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


class UpdateWeekDaySectionSerializer(serializers.Serializer):
    weeks = serializers.IntegerField(min_value=1, default=1)
    days = serializers.IntegerField(min_value=1, default=5)
    sections = serializers.IntegerField(min_value=1, default=5)


class CreateClassRoomSerializer(serializers.Serializer):
    college = serializers.CharField(max_length=255)
    floor = serializers.IntegerField(min_value=1)
    capacity = serializers.IntegerField(min_value=1)
    room_id = serializers.CharField(max_length=20)


class CreateCourseSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    total_period_number = serializers.IntegerField(min_value=1)
    capacity = serializers.IntegerField(min_value=1)

    class_room_ids = serializers.ListField(allow_null=True, allow_empty=True)

    def validate(self, data):
        teacher = User.objects.filter(id=data['teacher_id'], user_type=UserType.TEACHER).first()
        if not teacher:
            raise serializers.ValidationError("teacher ({}) does not exist.".format(data['teacher_id']))
        for cid in data['class_room_ids']:
            class_room = ClassRoom.objects.filter(id=cid)
            if not class_room:
                raise serializers.ValidationError("class room ({}) does not exist.".format(cid))
        return data


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['college', 'floor', 'capacity', 'room_id']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'total_period_number', 'capacity']
