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
        '''
        一个人只能负责一个SRTP项目
        '''
        PIC = User.objects.filter(username=data['PIC_id'])
        if PIC is None:
            raise serializers.ValidationError("student ({}) does not exist!."
                                              .format(data['PIC_id']))
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC)
        if srtp_pro:
            raise serializers.ValidationError("student ({}) has been in charge of a SRTP project."
                                              .format(data['person_in_charge']))
        if data['create_year'] > data['end_year']:
            raise serializers.ValidationError("开始时间不能在结束时间之前!")
        return data


class SRTPProjectInitFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()