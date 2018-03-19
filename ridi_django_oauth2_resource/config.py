from django.conf import settings

from ridi_oauth2.introspector.dtos import JwtInfo


class _Settings:
    JWT_SECRET_NAME = 'RIDI_OAUTH2_JWT_SECRET'
    JWT_ALGORITHM_NAME = 'RIDI_OAUTH2_JWT_ALGORITHM'
    JWT_EXPIRE_MARGIN_NAME = 'RIDI_OAUTH2_JWT_EXPIRE_MARGIN'

    COOKIE_DOMAIN = 'RIDI_OAUTH2_COOKIE_DOMAIN'
    ACCESS_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_ACCESS_TOKEN_COOKIE_KEY'
    REFRESH_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_REFRESH_TOKEN_COOKIE_KEY'


class _Default:
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRE_MARGIN = 500

    COOKIE_DOMAIN = 'ridibooks.com'
    ACCESS_TOKEN_COOKIE_KEY = "ridi-at"
    REFRESH_TOKEN_COOKIE_KEY = "ridi-rt"


# JwtInfo
_RIDI_OAUTH2_JWT_SECRET = getattr(settings, _Settings.JWT_SECRET_NAME)
_RIDI_OAUTH2_JWT_ALGORITHM = getattr(settings, _Settings.JWT_ALGORITHM_NAME, _Default.JWT_ALGORITHM)
_RIDI_OAUTH2_JWT_EXPIRE_MARGIN = getattr(settings, _Settings.JWT_EXPIRE_MARGIN_NAME, _Default.JWT_EXPIRE_MARGIN)

_JWT_INFO = JwtInfo(
    secret=_RIDI_OAUTH2_JWT_SECRET, algorithm=_RIDI_OAUTH2_JWT_ALGORITHM, expire_margin=_RIDI_OAUTH2_JWT_EXPIRE_MARGIN
)

# Cookie
_RIDI_COOKIE_DOMAIN = getattr(settings, _Settings.COOKIE_DOMAIN, _Default.COOKIE_DOMAIN)
_RIDI_ACCESS_TOKEN_COOKIE_KEY = getattr(settings, _Settings.ACCESS_TOKEN_COOKIE_KEY, _Default.ACCESS_TOKEN_COOKIE_KEY)
_RIDI_REFRESH_TOKEN_COOKIE_KEY = getattr(settings, _Settings.REFRESH_TOKEN_COOKIE_KEY, _Default.REFRESH_TOKEN_COOKIE_KEY)


class RidiOAuth2Config:
    @staticmethod
    def get_jwt_info() -> JwtInfo:
        return _JWT_INFO

    @staticmethod
    def get_cookie_domain() -> str:
        return _RIDI_COOKIE_DOMAIN

    @staticmethod
    def get_access_token_cookie_key() -> str:
        return _RIDI_ACCESS_TOKEN_COOKIE_KEY

    @staticmethod
    def get_refresh_token_cookie_key() -> str:
        return _RIDI_REFRESH_TOKEN_COOKIE_KEY
