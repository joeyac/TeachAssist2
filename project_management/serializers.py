from rest_framework import serializers
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage
from project_management.models import *
from account.models import User


class SRTPProjectCreationSerializer(serializers.ModelSerializer):
    # pro_state = serializers.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    PIC_id = serializers.IntegerField()

    class Meta:
        model = SRTPProject
        exclude = ('file1', 'update_time', 'pro_state', 'file2', 'file3', 'file4', 'person_in_charge')

    def validate(self, data):

        PIC = User.objects.filter(id=data['PIC_id']).first()
        if PIC is None:
            raise serializers.ValidationError("student ({}) does not exist!."
                                              .format(PIC.username))
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC)
        if srtp_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(PIC.username))
        if data['create_year'] > data['end_year']:
            raise serializers.ValidationError("开始时间不能在结束时间之前!")

        return data


class SRTPFindSerializer(serializers.Serializer):
    PIC_id = serializers.IntegerField()

    def validate(self, data):
        PIC = User.objects.filter(id=data['PCI_id']).first()
        if PIC is None:
            raise serializers.ValidationError("student ({}) does not exist!."
                                              .format(PIC.username))
        return data


class SRTPProjectFileUploadSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    file = serializers.FileField()
    pro_stage = serializers.ChoiceField(choices=ProStage.model_choices())
    PIC_id = serializers.IntegerField()

    def validate(self, data):
        if data['file'] is None:
            raise serializers.ValidationError("No file")
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))
        PCI = User.objects.get(id=data['PCI_id'])
        if srtp_pro.person_in_charge.id != PCI.id:
            raise serializers.ValidationError("user is not in charge of the project({})".format(srtp_pro.pro_name))
        return data


class SRTPUpdateSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    members = serializers.CharField(max_length=500, allow_null=True)
    instructor = serializers.CharField(max_length=32, allow_null=True)
    introduction = serializers.CharField(max_length=2000, allow_null=True)
    PIC_id = serializers.IntegerField()

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))
        PCI = User.objects.get(id=data['PIC_id'])
        if srtp_pro.person_in_charge.id != PCI.id:
            raise serializers.ValidationError("user is not in charge of the project({})".format(srtp_pro.pro_name))
        return data

# ----------------秘书-----------------------------------


class SRTPStateChangeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    pro_state = serializers.ChoiceField(choices=ProState.model_choices())


class SRTPGetSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(srtp_pro.pro_name))

# -------------毕业设计----------------------


class GraProjectCreationSerializer(serializers.ModelSerializer):
    PIC_id = serializers.IntegerField()

    class Meta:
        model = GraProject
        exclude = ('file1', 'file2', 'file3', 'file4', 'file5', 'update_time')
