from rest_framework import serializers
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage


class SRTPProjectCreationSerializer(serializers.Serializer):
    # pro_state = serializers.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    pro_level = serializers.ChoiceField(default=ProLevel.COLLEGE, choices=ProLevel.model_choices())
    file = serializers.FileField()



class SRTPProjectInitFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()