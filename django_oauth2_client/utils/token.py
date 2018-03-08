import typing

from django.http import HttpRequest

from django_oauth2_client.config import RidiOAuth2Config
from oauth2_client.constants import OAuth2GrantType
from oauth2_client.dtos import AccessTokenInfo, TokenData
from oauth2_client.exceptions import AuthorizationException, ExpireTokenException, InvalidJwtSignatureException, \
    OAuthFailureException
from oauth2_client.introspetor.jwt_introspector import JwtIntrospector
from oauth2_client.oauth2.factory import OAuth2GrantFactory


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


def refresh_access_token(refresh_token: str) -> typing.Optional[TokenData]:
    client_info = RidiOAuth2Config.get_client_info()
    auth_server_info = RidiOAuth2Config.get_auth_server_info()

    try:
        refresh_grant = OAuth2GrantFactory.get_grant(
            grant_type=OAuth2GrantType.REFRESH_TOKEN, client_info=client_info, auth_server_info=auth_server_info
        )
        return refresh_grant.get_access_token(refresh_token=refresh_token)
    except (AuthorizationException, OAuthFailureException):
        return None


def _get_access_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_access_token_cookie_key())


def _get_refresh_token_from_cookie(request: HttpRequest) -> str:
    return request.COOKIES.get(RidiOAuth2Config.get_refresh_token_cookie_key())
