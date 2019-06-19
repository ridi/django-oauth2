import typing

from django.http import HttpRequest

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_oauth2.client.dtos import TokenData
from ridi_oauth2.introspector.dtos import AccessTokenInfo
from ridi_oauth2.introspector.exceptions import ExpireTokenException, InvalidJwtSignatureException, InvalidToken
from ridi_oauth2.introspector.helpers import JwtIntrospectHelper


def get_token_from_cookie(request: HttpRequest) -> TokenData:
    return TokenData.from_dict({
        'access_token': _get_access_token_from_cookie(request=request),
        'refresh_token': _get_refresh_token_from_cookie(request=request),
    })


def get_token_info(token: str) -> typing.Optional[AccessTokenInfo]:
    jwt_infos = RidiOAuth2Config.get_jwt_infos()
    try:
        token_info = JwtIntrospectHelper.introspect(jwt_infos, token)

    except (KeyError, ExpireTokenException, InvalidJwtSignatureException, InvalidToken):
        token_info = None

    return token_info


def _get_access_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_access_token_cookie_key())


def _get_refresh_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_refresh_token_cookie_key())
