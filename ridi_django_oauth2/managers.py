from django.contrib.auth.base_user import BaseUserManager

from ridi_django_oauth2.exceptions import ImpossibleSetSuperuserException


class RidiUserManager(BaseUserManager):
    def create_user(self, u_idx: int, **kwargs):
        ridi_user = self.model(u_idx=u_idx, **kwargs)
        ridi_user.set_unusable_password()
        ridi_user.save()

        return ridi_user

    def create_superuser(self, u_idx: int, **kwargs):
        raise ImpossibleSetSuperuserException
