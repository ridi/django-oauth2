from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2.response import HttpUnauthorizedResponse
from ridi_django_oauth2.utils.token import get_token_from_cookie, get_token_info
from ridi_oauth2.client.dtos import TokenData
from ridi_oauth2.introspector.dtos import AccessTokenInfo
from ridi_oauth2.introspector.exceptions import PublicKeyException


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = AnonymousUser()

        token = get_token_from_cookie(request=request)
        token_info = None
        if token.access_token:
            try:
                token_info = get_token_info(token.access_token.token)
            except PublicKeyException:
                return HttpUnauthorizedResponse()

        if token_info is not None:
            self._set_user_in_request(request, token_info, token)

        return None

    @staticmethod
    def _set_user_in_request(request, token_info: AccessTokenInfo, token: TokenData):
        get_user_from_token_info = RidiOAuth2Config.get_user_from_token_info_callable()

        if get_user_from_token_info:
            user = get_user_from_token_info(token_info)

        else:
            user, _ = get_user_model().objects.get_or_create(u_idx=token_info.u_idx)

        user.token = token
        user.token_info = token_info
        request.user = user
