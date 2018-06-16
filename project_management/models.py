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

    file1 = models.FilePathField(null=True)
    file2 = models.FilePathField(null=True)
    file3 = models.FilePathField(null=True)
    file4 = models.FilePathField(null=True)

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

    file1 = models.FilePathField()
    file2 = models.FilePathField(null=True)
    file3 = models.FilePathField(null=True)
    file4 = models.FilePathField(null=True)

    pro_name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=2000)

    def toDict(self):
        lst = []
        for attr in self._meta.fields:
            lst.append((attr.name, str(getattr(self, attr.name))))
        return dict(lst)


class GraProject(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    create_year = models.DateField()
    end_year = models.DateField()

    teacher = models.ForeignKey(User, related_name='teacher_gra', on_delete=models.CASCADE)
    student = models.OneToOneField(User, related_name='student_gra', on_delete=models.CASCADE)

    file1 = models.FilePathField(null=True)
    file2 = models.FilePathField(null=True)
    file3 = models.FilePathField(null=True)

    file4 = models.FilePathField(null=True)
    file5 = models.FilePathField(null=True)

    pro_name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=2000)

    def toDict(self):
        lst = []
        for attr in self._meta.fields:
            lst.append((attr.name, str(getattr(self, attr.name))))
        return dict(lst)
