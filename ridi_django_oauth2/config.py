from django.conf import settings

from ridi_oauth2.client.dtos import KeyAuthInfo


class _SettingKeyName:
    INTERNAL_AUTH_ISS = 'RIDI_OAUTH2_INTERNAL_AUTH_ISS'
    INTERNAL_AUTH_AUD = 'RIDI_OAUTH2_INTERNAL_AUTH_AUD'
    INTERNAL_AUTH_TTL_SECONDS = 'RIDI_OAUTH2_INTERNAL_AUTH_TTL_SECONDS'
    INTERNAL_AUTH_ALG = 'RIDI_OAUTH2_INTERNAL_AUTH_ALG'
    INTERNAL_AUTH_URL = 'RIDI_OAUTH2_INTERNAL_AUTH_URL'
    INTERNAL_AUTH_PRIVATE_KEY = 'RIDI_OAUTH2_INTERNAL_AUTH_PRIVATE_KEY'

    COOKIE_DOMAIN = 'RIDI_OAUTH2_COOKIE_DOMAIN'
    ACCESS_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_ACCESS_TOKEN_COOKIE_KEY'
    REFRESH_TOKEN_COOKIE_KEY = 'RIDI_OAUTH2_REFRESH_TOKEN_COOKIE_KEY'


class _Default:
    COOKIE_DOMAIN = 'ridibooks.com'
    ACCESS_TOKEN_COOKIE_KEY = "ridi-at"
    REFRESH_TOKEN_COOKIE_KEY = "ridi-rt"


# Cookie
_RIDI_COOKIE_DOMAIN = getattr(settings, _SettingKeyName.COOKIE_DOMAIN, _Default.COOKIE_DOMAIN)
_RIDI_ACCESS_TOKEN_COOKIE_KEY = getattr(settings, _SettingKeyName.ACCESS_TOKEN_COOKIE_KEY, _Default.ACCESS_TOKEN_COOKIE_KEY)
_RIDI_REFRESH_TOKEN_COOKIE_KEY = getattr(settings, _SettingKeyName.REFRESH_TOKEN_COOKIE_KEY, _Default.REFRESH_TOKEN_COOKIE_KEY)

# Default Key Auth Info
_RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_AUD = 'account'
_RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_ALG = 'RS256'
_RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_TTL_SECONDS = 60

# Key Auth Info
_RIDI_OAUTH2_KEY_AUTH_INFO = KeyAuthInfo({
    'iss': getattr(settings, _SettingKeyName.INTERNAL_AUTH_ISS),
    'aud': getattr(settings, _SettingKeyName.INTERNAL_AUTH_AUD, _RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_AUD),
    'ttl_seconds': getattr(settings, _SettingKeyName.INTERNAL_AUTH_TTL_SECONDS, _RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_TTL_SECONDS),
    'alg': getattr(settings, _SettingKeyName.INTERNAL_AUTH_ALG, _RIDI_OAUTH2_KEY_AUTH_INFO_DEFAULT_ALG),
    'url': getattr(settings, _SettingKeyName.INTERNAL_AUTH_URL),
    'secret': getattr(settings, _SettingKeyName.INTERNAL_AUTH_PRIVATE_KEY),
})


class RidiOAuth2Config:
    @staticmethod
    def get_internal_key_auth_info() -> KeyAuthInfo:
        return _RIDI_OAUTH2_KEY_AUTH_INFO

    @staticmethod
    def get_cookie_domain() -> str:
        return _RIDI_COOKIE_DOMAIN

    @staticmethod
    def get_access_token_cookie_key() -> str:
        return _RIDI_ACCESS_TOKEN_COOKIE_KEY

    @staticmethod
    def get_refresh_token_cookie_key() -> str:
        return _RIDI_REFRESH_TOKEN_COOKIE_KEY
