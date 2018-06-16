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
        exclude = ('file1', 'update_time', 'pro_state', 'file2', 'file3', 'file4', 'person_in_charge')

    def validate(self, data):

        PIC = User.objects.filter(username=data['username']).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC)
        if srtp_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(PIC.username))
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
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))
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


class SRTPGetSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))

# -------------毕业设计----------------------


class GraProjectCreationSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GraProject
        exclude = ('file1', 'file2', 'file3', 'file4', 'file5', 'update_time')
