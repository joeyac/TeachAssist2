from rest_framework import serializers
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage
from project_management.models import SRTPProject
from account.models import User


class SRTPProjectCreationSerializer(serializers.ModelSerializer):
    # pro_state = serializers.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    PIC_id = serializers.CharField(max_length=32)

    class Meta:
        model = SRTPProject
        exclude = ('update_time', 'pro_state', 'file2', 'file3', 'person_in_charge')

    def validate(self, data):

        PIC = User.objects.filter(username=data['PIC_id']).first()
        if PIC is None:
            raise serializers.ValidationError("student ({}) does not exist!."
                                              .format(data['PIC_id']))
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC)
        if srtp_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(data['PIC_id']))
        if data['create_year'] > data['end_year']:
            raise serializers.ValidationError("开始时间不能在结束时间之前!")
        if data['file1'] is None:
            raise serializers.ValidationError('No file!')
        return data


class SRTPFindSerializer(serializers.Serializer):
    PCI_id = serializers.CharField(max_length=32)

    def validate(self, value):
        PIC = User.objects.filter(username=value).first()
        if PIC is None:
            raise serializers.ValidationError("student ({}) does not exist!."
                                              .format(value))
        return value


class SRTPProjectFileUploadSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    file = serializers.FileField()
    pro_stage = serializers.ChoiceField(choices=ProStage.model_choices())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['file'] is None:
            raise serializers.ValidationError("No file")
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(data['pro_id']))
        if srtp_pro.person_in_charge is not data['user']:
            raise serializers.ValidationError("user is not in charge of the project({})".format(data['pro_id']))
        return data


class SRTPUpdateSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    members = serializers.CharField(max_length=500, allow_null=True)
    instructor = serializers.CharField(max_length=32, allow_null=True)
    introduction = serializers.CharField(max_length=2000, allow_null=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
        if srtp_pro is None:
            raise serializers.ValidationError("no project ({})".format(data['pro_id']))
        if srtp_pro.person_in_charge is not data['user']:
            raise serializers.ValidationError("user is not in charge of the project({})".format(data['pro_id']))
        return data
