from rest_framework import serializers
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage, OperationCode
from project_management.models import *
from account.models import User
import os
from django.conf import settings


class SRTPProjectCreationSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.FilePathField(settings.MEDIA_ROOT)

    class Meta:
        model = SRTPProject
        exclude = ('apply_file', 'update_time', 'pro_state', 'middle_file', 'end_file', 'abnormal_file', 'person_in_charge')

    def validate(self, data):

        PIC = User.objects.filter(username=data['username']).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC)
        if srtp_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(PIC.real_name))
        if data['create_year'] > data['end_year']:
            raise serializers.ValidationError("开始时间不能在结束时间之前!")

        return data


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SRTPUpdateSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    members = serializers.CharField(max_length=500, required=False, allow_null=True)
    instructor = serializers.CharField(max_length=32, required=False, allow_null=True)
    introduction = serializers.CharField(max_length=2000, required=False, allow_null=True)
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.CharField(max_length=200, required=False, allow_null=True)
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("project ({}) does not exist!".format(srtp_pro.pro_name))
        PCI = User.objects.get(username=data['username'])
        if srtp_pro.person_in_charge.id != PCI.id:
            raise serializers.ValidationError("user is not in charge of the project({})".format(srtp_pro.pro_name))
        try:
            file_url = data['file_url']
            if data['op_code'] == OperationCode.UPDATE:
                raise serializers.ValidationError("Operation error!")
            if not os.path.exists(file_url):
                raise serializers.ValidationError("file({}) does not exist!".format(file_url))
        except:
            if data['op_code'] != OperationCode.UPDATE:
                raise serializers.ValidationError("File Needed")
        return data

# ----------------秘书-----------------------------------


class SRTPStateChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())


class SRTPLevelChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    pro_level = serializers.ChoiceField(choices=ProLevel.model_choices())


class SRTPGetALLSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))
        return data


class EduStateChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())


class EduLevelChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    pro_level = serializers.ChoiceField(choices=ProLevel.model_choices())


class EduGetALLSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()

    def validate(self, data):
        edu_pro = EduProject.objects.filter(id=data['pro_id']).first()
        if edu_pro is None:
            raise serializers.ValidationError("no project ({})".format(edu_pro.pro_name))
        return data

# -------------毕业设计----------------------


class GraCreationSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField(max_length=32)
    student_username = serializers.CharField(max_length=32)
    file_url = serializers.FilePathField(settings.MEDIA_ROOT)

    class Meta:
        model = GraProject
        exclude = ('select_file', 'start_file', 'end_file', 'task_file', 'check_file', 'update_time', 'student', 'pro_state', 'teacher')

    def validate(self, data):
        teacher = User.objects.filter(username=data['teacher_username']).first()
        if teacher is None:
            raise serializers.ValidationError("teacher({}) does not exist!".format(data['teacher_username']))
        student = User.objects.filter(username=data['student_username']).first()
        gra_pro = GraProject.objects.filter(student=student).first()
        if gra_pro is not None:
            raise serializers.ValidationError("student({}) has already had a graduation project!".format(student.username))

        # file_url = data['select_file']
        return data


class GraUpdateSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.FilePathField(settings.MEDIA_ROOT)
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())

    def validate(self, data):
        gra_pro = GraProject.objects.filter(id=data['pro_id']).first()
        if gra_pro is None:
            raise serializers.ValidationError("project({}) does not exist!".format(data['pro_id']))
        if gra_pro.student.username != str(data['username']):
            raise serializers.ValidationError("project id ({}) error!".format(data['pro_id']))
        return data


class GraStateChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.FilePathField(settings.MEDIA_ROOT)
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())

    def validate(self, data):
        gra_pro = GraProject.objects.filter(id=data['pro_id']).first()
        if gra_pro is None:
            raise serializers.ValidationError("project({}) does not exist!".format(data['pro_id']))
        if gra_pro.teacher.username != str(data['username']):
            raise serializers.ValidationError("project id ({}) error!".format(data['pro_id']))
        return data


# ----------------教改--------------------------
class EduCreationSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.FilePathField(settings.MEDIA_ROOT)

    class Meta:
        model = EduProject
        exclude = ('apply_file', 'update_time', 'pro_state', 'middle_file', 'end_file', 'abnormal_file', 'person_in_charge')

    def validate(self, data):

        PIC = User.objects.filter(username=data['username']).first()
        edu_pro = EduProject.objects.filter(person_in_charge=PIC).first()
        if edu_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(PIC.real_name))
        if data['create_year'] > data['end_year']:
            raise serializers.ValidationError("开始时间不能在结束时间之前!")
        return data


class EduUpdateSerializer(serializers.Serializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pro_id = serializers.IntegerField()
    members = serializers.CharField(max_length=500, required=False, allow_null=True)
    introduction = serializers.CharField(max_length=2000, required=False, allow_null=True)
    file_url = serializers.CharField(max_length=200, required=False, allow_null=True)
    op_code = serializers.ChoiceField(choices=OperationCode.model_choices())

    def validate(self, data):
        edu_pro = EduProject.objects.filter(id=data['pro_id']).first()
        if edu_pro is None:
            raise serializers.ValidationError("project ({}) does not exist!".format(edu_pro.pro_name))
        PCI = User.objects.get(username=data['username'])
        if edu_pro.person_in_charge.id != PCI.id:
            raise serializers.ValidationError("user is not in charge of the project({})".format(edu_pro.pro_name))
        try:
            file_url = data['file_url']
            if data['op_code'] == OperationCode.UPDATE:
                raise serializers.ValidationError("Operation error!")
            if not os.path.exists(file_url):
                raise serializers.ValidationError("file({}) does not exist!".format(file_url))
        except:
            if data['op_code'] != OperationCode.UPDATE:
                raise serializers.ValidationError("File Needed")
        return data




