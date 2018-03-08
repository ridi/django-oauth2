from django.conf import settings

from oauth2_client.introspetor.dtos import JwtInfo
from oauth2_client.oauth2.dtos import AuthorizationServerInfo, ClientInfo


class _Settings:
    CLIENT_ID = 'RIDI_OAUTH2_CLIENT_ID'
    CLIENT_SECRET = 'RIDI_OAUTH2_CLIENT_SECRET'
    SCOPE = 'RIDI_OAUTH2_SCOPE'
    REDIRECT_URI = 'RIDI_OAUTH2_REDIRECT_URI'

    AUTHORIZATION_URL = 'RIDI_OAUTH2_AUTHORIZATION_URL'
    TOKEN_URL = 'RIDI_OAUTH2_TOKEN_URL'

    JWT_SECRET_NAME = 'RIDI_OAUTH2_JWT_SECRET'
    JWT_ALGORITHM_NAME = 'RIDI_OAUTH2_JWT_ALGORITHM'
    JWT_EXPIRE_TERM_NAME = 'RIDI_OAUTH2_JWT_EXPIRE_TERM'

    COOKIE_DOMAIN = 'RIDI_OAUTH2_COOKIE_DOMAIN'
    ACCESS_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_ACCESS_TOKEN_COOKIE_KEY'
    REFRESH_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_REFRESH_TOKEN_COOKIE_KEY'


class _Default:
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRE_TERM = 500

    COOKIE_DOMAIN = 'ridibooks.com'
    ACCESS_TOKEN_COOKIE_KEY = "ridi-at"
    REFRESH_TOKEN_COOKIE_KEY = "ridi-rt"


# ClientInfo
_RIDI_OAUTH2_CLIENT_ID = getattr(settings, _Settings.CLIENT_ID)
_RIDI_OAUTH2_CLIENT_SECRET = getattr(settings, _Settings.CLIENT_SECRET)
_RIDI_OAUTH2_SCOPE = getattr(settings, _Settings.SCOPE, None)
_RIDI_OAUTH2_REDIRECT_URI = getattr(settings, _Settings.REDIRECT_URI, None)

_CLIENT_INFO = ClientInfo(
    client_id=_RIDI_OAUTH2_CLIENT_ID, client_secret=_RIDI_OAUTH2_CLIENT_SECRET, scope=_RIDI_OAUTH2_SCOPE,
    redirect_uri=_RIDI_OAUTH2_REDIRECT_URI
)

# AuthServerInfo
_RIDI_OAUTH2_AUTHORIZATION_URL = getattr(settings, _Settings.AUTHORIZATION_URL)
_RIDI_OAUTH2_TOKEN_URL = getattr(settings, _Settings.TOKEN_URL)

_AUTH_SERVER_INFO = AuthorizationServerInfo(authorization_url=_RIDI_OAUTH2_AUTHORIZATION_URL, token_url=_RIDI_OAUTH2_TOKEN_URL)

# JwtInfo
_RIDI_OAUTH2_JWT_SECRET = getattr(settings, _Settings.JWT_SECRET_NAME)
_RIDI_OAUTH2_JWT_ALGORITHM = getattr(settings, _Settings.JWT_ALGORITHM_NAME, _Default.JWT_ALGORITHM)
_RIDI_OAUTH2_JWT_EXPIRE_TERM = getattr(settings, _Settings.JWT_EXPIRE_TERM_NAME, _Default.JWT_EXPIRE_TERM)

_JWT_INFO = JwtInfo(
    secret=_RIDI_OAUTH2_JWT_SECRET, algorithm=_RIDI_OAUTH2_JWT_ALGORITHM, expire_term=_RIDI_OAUTH2_JWT_EXPIRE_TERM
)

# Cookie
_RIDI_COOKIE_DOMAIN = getattr(settings, _Settings.COOKIE_DOMAIN, _Default.COOKIE_DOMAIN)
_RIDI_ACCESS_TOKEN_COOKIE_KEY = getattr(settings, _Settings.ACCESS_TOKEN_COOKIE_KEY, _Default.ACCESS_TOKEN_COOKIE_KEY)
_RIDI_REFRESH_TOKEN_COOKIE_KEY = getattr(settings, _Settings.REFRESH_TOKEN_COOKIE_KEY, _Default.REFRESH_TOKEN_COOKIE_KEY)


class RidiOAuth2Config:
    @staticmethod
    def get_client_info() -> ClientInfo:
        return _CLIENT_INFO

    @staticmethod
    def get_auth_server_info() -> AuthorizationServerInfo:
        return _AUTH_SERVER_INFO

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
