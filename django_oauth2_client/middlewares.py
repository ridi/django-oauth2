from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from django_oauth2_client.config import RidiOAuth2Config
from django_oauth2_client.constants import DEFAULT_ACCESS_TOKEN_EXPIRE, DEFAULT_REFRESH_TOKEN_EXPIRE
from django_oauth2_client.utils.token import get_token_from_cookie, get_token_info, refresh_access_token


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = AnonymousUser()

        token = get_token_from_cookie(request=request)
        token_info = None
        if token.access_token:
            token_info = get_token_info(token.access_token.token)

        if token_info is None and token.refresh_token:
            request._token = refresh_access_token(  # flake8: noqa: W0212  # pylint:disable=protected-access
                refresh_token=token.refresh_token.token  # flake8: noqa: W0212  # pylint:disable=protected-access
            )
            if request._token:  # flake8: noqa: W0212  # pylint:disable=protected-access
                token_info = get_token_info(request._token.access_token.token)  # flake8: noqa: W0212  # pylint:disable=protected-access

        if token_info is not None:
            user, _ = get_user_model().objects.get_or_create(u_idx=token_info.u_idx)
            user.token = token
            user.token_info = token_info
            request.user = user

        return None

    def process_response(self, request, response):
        token = getattr(request, '_token', None)

        if token:
            if token.access_token:
                response.set_cookie(
                    key=RidiOAuth2Config.get_access_token_cookie_key(), value=token.access_token,
                    secure=True, httponly=True, max_age=token.access_token.expires_in or DEFAULT_ACCESS_TOKEN_EXPIRE,
                    domain=RidiOAuth2Config.get_cookie_domain(),
                )

            if token.refresh_token:
                response.set_cookie(
                    key=RidiOAuth2Config.get_refresh_token_cookie_key(), value=token.refresh_token,
                    secure=True, httponly=True, max_age=token.refresh_token.expires_in or DEFAULT_REFRESH_TOKEN_EXPIRE,
                    domain=RidiOAuth2Config.get_cookie_domain(),
                )

        return response
