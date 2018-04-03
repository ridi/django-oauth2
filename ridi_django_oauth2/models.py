from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from ridi_django_oauth2.managers import RidiUserManager


class RidiUser(AbstractBaseUser):
    u_idx = models.IntegerField(primary_key=True, editable=False, verbose_name='u_idx')

    USERNAME_FIELD = 'u_idx'

    objects = RidiUserManager()

    class Meta:
        db_table = 'ridi_user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'

    def __str__(self):
        return str(self.get_username())
