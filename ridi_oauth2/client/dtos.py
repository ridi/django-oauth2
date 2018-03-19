import typing


class ClientInfo:
    def __init__(self, client_id: str, client_secret: str, scope: str=None, redirect_uri: str=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._redirect_uri = redirect_uri

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def redirect_uri(self) -> str:
        return self._redirect_uri


class AuthorizationServerInfo:
    def __init__(self, authorization_url: str=None, token_url: str=None):
        self._authorization_url = authorization_url
        self._token_url = token_url

    @property
    def authorization_url(self) -> str:
        return self._authorization_url

    @property
    def token_url(self) -> str:
        return self._token_url


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
