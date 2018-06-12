from django.db import models

# Create your models here.
from utils.constants import FileType, ProType, ProState, ProLevel, ProStage
import django.utils.timezone as timezone
from time import strftime
from account.models import User


class SRTPProject(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    pro_state = models.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())
    students = models.ManyToManyField(User, related_name='students_srtp')

    file1 = models.FileField()
    file2 = models.FileField()
    file3 = models.FileField()


class EduProject(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    pro_state = models.CharField(max_length=10, default=ProState.RUNNING, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())

    members = models.ManyToManyField(User)

    file1 = models.FileField()
    file2 = models.FileField()
    file3 = models.FileField()


class GraProject(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True, null=True)
    teacher = models.ForeignKey(User, related_name='teacher_gra', on_delete=models.CASCADE, null=True)
    student = models.OneToOneField(User, related_name='student_gra', on_delete=models.CASCADE, null=True)

    file1 = models.FileField()
    file2 = models.FileField()
    file3 = models.FileField()
