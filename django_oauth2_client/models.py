from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from django_oauth2_client.managers import RidiUserManager


class RidiUser(AbstractBaseUser):
    u_idx = models.AutoField(primary_key=True, editable=False, verbose_name='u_idx')

    USERNAME_FIELD = 'u_idx'

    objects = RidiUserManager()

    class Meta:
        db_table = 'ridi_user'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정 리스트'
