from django.conf import settings


class _SettingKeyName:
    KEY_URL = 'RIDI_OAUTH2_KEY_URL'
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

_RIDI_OAUTH2_KEY_URL = getattr(settings, _SettingKeyName.KEY_URL)


class RidiOAuth2Config:
    @staticmethod
    def get_key_url() -> str:
        return _RIDI_OAUTH2_KEY_URL

    @staticmethod
    def get_cookie_domain() -> str:
        return _RIDI_COOKIE_DOMAIN

    @staticmethod
    def get_access_token_cookie_key() -> str:
        return _RIDI_ACCESS_TOKEN_COOKIE_KEY

    @staticmethod
    def get_refresh_token_cookie_key() -> str:
        return _RIDI_REFRESH_TOKEN_COOKIE_KEY
