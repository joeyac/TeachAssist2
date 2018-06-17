from django.db import models

# Create your models here.
from utils.constants import ProState, ProLevel
from time import strftime
from account.models import User


class SRTPProject(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    create_year = models.DateField()
    end_year = models.DateField()

    pro_state = models.CharField(max_length=10, default=ProState.UNCONFIRMED, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())

    person_in_charge = models.ForeignKey(User, related_name='PIC_srtp', on_delete=models.CASCADE)
    members = models.CharField(max_length=500)
    instructor = models.CharField(max_length=32)

    apply_file = models.FilePathField(null=True)
    middle_file = models.FilePathField(null=True)
    end_file = models.FilePathField(null=True)
    abnormal_file = models.FilePathField(null=True)

    pro_name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=2000)

    def toDict(self):
        lst = []
        for attr in self._meta.fields:
            lst.append((attr.name, str(getattr(self, attr.name))))
        return dict(lst)


class EduProject(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    create_year = models.DateField()
    end_year = models.DateField()

    pro_state = models.CharField(max_length=10, default=ProState.UNCONFIRMED, choices=ProState.model_choices())
    pro_level = models.CharField(max_length=10, default=ProLevel.COLLEGE, choices=ProLevel.model_choices())

    person_in_charge = models.ForeignKey(User, related_name='PIC_edu', on_delete=models.CASCADE)
    members = models.CharField(max_length=500)

    apply_file = models.FilePathField()
    middle_file = models.FilePathField(null=True)
    end_file = models.FilePathField(null=True)
    abnormal_file = models.FilePathField(null=True)

    pro_name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=2000)

    def toDict(self):
        lst = []
        for attr in self._meta.fields:
            lst.append((attr.name, str(getattr(self, attr.name))))
        return dict(lst)


class GraProject(models.Model):
    update_time = models.DateTimeField(auto_now=True)

    teacher = models.ForeignKey(User, related_name='teacher_gra', on_delete=models.CASCADE)
    student = models.OneToOneField(User, related_name='student_gra', on_delete=models.CASCADE)

    select_file = models.FilePathField(null=True)
    start_file = models.FilePathField(null=True)
    end_file = models.FilePathField(null=True)

    task_file = models.FilePathField(null=True)
    check_file = models.FilePathField(null=True)

    pro_name = models.CharField(max_length=100)
    pro_state = models.CharField(max_length=10, default=ProState.UNCONFIRMED, choices=ProState.model_choices())

    def toDict(self):
        lst = []
        for attr in self._meta.fields:
            lst.append((attr.name, str(getattr(self, attr.name))))
        return dict(lst)
