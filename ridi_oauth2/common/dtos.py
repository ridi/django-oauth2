import typing


class Token:
    def __init__(self, token: str, expires_in: int=None):
        self._token = token
        self._expires_in = expires_in

    @property
    def token(self) -> str:
        return self._token

    @property
    def expires_in(self) -> int:
        return self._expires_in


class TokenData:
    def __init__(self, access_token: Token, token_type: str=None, scope: str=None, refresh_token: Token=None):
        self._access_token = access_token
        self._token_type = token_type
        self._scope = scope

        self._refresh_token = refresh_token

    @property
    def access_token(self) -> Token:
        return self._access_token

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def refresh_token(self) -> Token:
        return self._refresh_token

    @staticmethod
    def from_dict(dictionary: typing.Dict):
        access_token = None
        if dictionary.get('access_token', None):
            access_token = Token(token=dictionary['access_token'], expires_in=dictionary.get('expires_in', None))

        refresh_token = None
        if dictionary.get('refresh_token', None):
            refresh_token = Token(token=dictionary['refresh_token'], expires_in=dictionary.get('refresh_token_expires_in', None))

        return TokenData(
            access_token=access_token, token_type=dictionary.get('token_type', None), scope=dictionary.get('scope', None),
            refresh_token=refresh_token
        )
