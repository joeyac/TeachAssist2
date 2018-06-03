from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.constants import UserType


class User(AbstractUser):
    user_type = models.CharField(max_length=10, default=UserType.STUDENT, choices=UserType.model_choices())

