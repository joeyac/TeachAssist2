from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.constants import UserType
from project_management.models import SRTPProject, EduProject, GraProject


class User(AbstractUser):
    user_type = models.CharField(max_length=10, default=UserType.STUDENT, choices=UserType.model_choices())