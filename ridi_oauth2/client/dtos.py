

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
