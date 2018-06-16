from django.db.models import Max
from rest_framework import serializers
from course_arrangement.models import *


class WeekDaySlotSerializer(serializers.Serializer):
    week = serializers.IntegerField(default=4)
    day = serializers.IntegerField(default=5)
    slot = serializers.IntegerField(default=5)

    def validate(self, data):
        if data['week'] <= 0 or data['day'] <= 0 or data['slot'] <= 0:
            raise serializers.ValidationError("all value should be positive value")

        week_max = Course.objects.aggregate(val=Max('start_week', 'end_week'))['val']
        if data['week'] < week_max:
            raise serializers.ValidationError(
                "day value({}) should no less than any course week({})".format(data['week'], week_max))

        if data['day'] > 5:
            raise serializers.ValidationError("day value({}) should less than 5".format(data['day']))
        if data['slot'] > 5:
            raise serializers.ValidationError("slot value({}) should less than 5".format(data['slot']))
        return data


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['college', 'floor', 'capacity', 'room_id']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'total_period_number', 'capacity']


class SpecialCourseSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(label='name')
    teacher = serializers.StringRelatedField()
    week_str = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = ['full_name', 'week_str', 'teacher']


class AssignmentSerializer(serializers.ModelSerializer):
    classroom_name = serializers.ReadOnlyField(label='classroom')
    course = SpecialCourseSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ['day', 'slot', 'classroom_name', 'course']


class TeacherAssignmentSerializer(serializers.Serializer):
    tid = serializers.IntegerField()

    def validate(self, data):
        instance = User.objects.all().filter(id=data['tid'], user_type=UserType.TEACHER).first()
        if not instance:
            raise serializers.ValidationError("no such teacher: {}".format(data['tid']))
        return data


class ClassRoomAssignmentSerializer(serializers.Serializer):
    rid = serializers.IntegerField()

    def validate(self, data):
        instance = ClassRoom.objects.all().filter(id=data['rid']).first()
        if not instance:
            raise serializers.ValidationError("no such class room: {}".format(data['rid']))
        return data


class ClassAssignmentSerializer(serializers.Serializer):
    cid = serializers.IntegerField()

    def validate(self, data):
        instance = Class.objects.all().filter(id=data['cid']).first()
        if not instance:
            raise serializers.ValidationError("no such class: {}".format(data['cid']))
        return data
