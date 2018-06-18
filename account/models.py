from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from utils.constants import UserType


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    real_name = models.CharField(max_length=255, default='佚名')
    user_type = models.CharField(max_length=10, default=UserType.STUDENT, choices=UserType.model_choices())

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.username)
