from typing import Dict

from django.conf import settings

from ridi_oauth2.introspector.dtos import JwtInfo


class _Settings:
    JWT_SECRETS = 'RIDI_OAUTH2_JWT_SECRETS'

    COOKIE_DOMAIN = 'RIDI_OAUTH2_COOKIE_DOMAIN'
    ACCESS_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_ACCESS_TOKEN_COOKIE_KEY'
    REFRESH_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_REFRESH_TOKEN_COOKIE_KEY'


class _Default:
    COOKIE_DOMAIN = 'ridibooks.com'
    ACCESS_TOKEN_COOKIE_KEY = "ridi-at"
    REFRESH_TOKEN_COOKIE_KEY = "ridi-rt"


# JwtInfo
_RIDI_OAUTH2_JWT_SECRETS = getattr(settings, _Settings.JWT_SECRETS)
_JWT_INFOS = dict([
    (_RIDI_OAUTH2_JWT_SECRET['kid'], JwtInfo(_RIDI_OAUTH2_JWT_SECRET['secret'], _RIDI_OAUTH2_JWT_SECRET['alg']))
    for _RIDI_OAUTH2_JWT_SECRET in _RIDI_OAUTH2_JWT_SECRETS
])

# Cookie
_RIDI_COOKIE_DOMAIN = getattr(settings, _Settings.COOKIE_DOMAIN, _Default.COOKIE_DOMAIN)
_RIDI_ACCESS_TOKEN_COOKIE_KEY = getattr(settings, _Settings.ACCESS_TOKEN_COOKIE_KEY, _Default.ACCESS_TOKEN_COOKIE_KEY)
_RIDI_REFRESH_TOKEN_COOKIE_KEY = getattr(settings, _Settings.REFRESH_TOKEN_COOKIE_KEY, _Default.REFRESH_TOKEN_COOKIE_KEY)


class RidiOAuth2Config:
    @staticmethod
    def get_jwt_infos() -> Dict[str, JwtInfo]:
        return _JWT_INFOS

    @staticmethod
    def get_cookie_domain() -> str:
        return _RIDI_COOKIE_DOMAIN

    @staticmethod
    def get_access_token_cookie_key() -> str:
        return _RIDI_ACCESS_TOKEN_COOKIE_KEY

    @staticmethod
    def get_refresh_token_cookie_key() -> str:
        return _RIDI_REFRESH_TOKEN_COOKIE_KEY
