from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.constants import UserType


class User(AbstractUser):
    real_name = models.CharField(max_length=255, default='佚名')
    user_type = models.CharField(max_length=10, default=UserType.STUDENT, choices=UserType.model_choices())

    def __str__(self):
        return "{}".format(self.real_name)
