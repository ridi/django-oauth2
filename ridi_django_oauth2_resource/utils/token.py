import typing

from django.http import HttpRequest

from ridi_django_oauth2_resource.config import RidiOAuth2Config
from ridi_oauth2.common.dtos import TokenData
from ridi_oauth2.introspetor.dtos import AccessTokenInfo
from ridi_oauth2.introspetor.exceptions import ExpireTokenException, InvalidJwtSignatureException
from ridi_oauth2.introspetor.jwt_introspector import JwtIntrospector


def get_token_from_cookie(request: HttpRequest) -> TokenData:
    return TokenData.from_dict({
        'access_token': _get_access_token_from_cookie(request=request),
        'refresh_token': _get_refresh_token_from_cookie(request=request),
    })


def get_token_info(token: str) -> typing.Optional[AccessTokenInfo]:
    try:
        result = JwtIntrospector(jwt_info=RidiOAuth2Config.get_jwt_info(), access_token=token).introspect()
        token_info = AccessTokenInfo.from_dict(dictionary=result)
    except (KeyError, ExpireTokenException, InvalidJwtSignatureException):
        token_info = None

    return token_info


def _get_access_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_access_token_cookie_key())


def _get_refresh_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_refresh_token_cookie_key())
