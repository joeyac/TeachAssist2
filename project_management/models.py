from django.db import models

# Create your models here.
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage
import django.utils.timezone as timezone
# import account.models


class SRTPProject(models.Model):
    crate_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, null=True)
    pro_state = models.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())


class File_Info(models.Model):
    file_name = models.CharField(max_length=50)
    file_url = models.CharField(max_length=50)
    file_type = models.CharField(max_length=10, default=FileType.ALL, choices=FileType.model_choices())
    project = models.ForeignKey(SRTPProject, on_delete=models.CASCADE)
    pro_stage = models.CharField(max_length=10, default=ProStage.INIT, choices=ProStage.model_choices())


class EduProject(models.Model):
    crate_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, null=True)
    pro_state = models.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())


class GraProject(models.Model):
    crate_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, null=True)
    # teacher = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # student = models.ForeignKey(User, null=True, on_delete=models.CASCADE)