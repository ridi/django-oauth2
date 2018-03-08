import typing

from django_oauth2_client.config import RidiOAuth2Config


def generate_cookie(access_token: str) -> typing.Dict:
    return {
        RidiOAuth2Config.get_access_token_cookie_key(): access_token
    }
