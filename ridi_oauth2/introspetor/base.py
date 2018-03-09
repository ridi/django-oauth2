import typing


class BaseIntrospector:
    def __init__(self, access_token: str, token_type_hint: str=None):
        self._access_token = access_token
        self._token_type_hint = token_type_hint

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def token_type_hint(self) -> str:
        return self._token_type_hint

    def introspect(self) -> typing.Dict:
        raise NotImplementedError
