import typing

from ridi_django_oauth2.config import RidiOAuth2Config


def generate_cookie(access_token: str) -> typing.Dict:
    return {
        RidiOAuth2Config.get_access_token_cookie_key(): access_token
    }
