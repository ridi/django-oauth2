

class InvalidResponseException(Exception):
    pass


class NotSupportedGrantException(Exception):
    pass


class OAuthFailureException(Exception):
    def __init__(self, error_code: str, *args, description: str=None, error_uri: str=None):
        self._error_code = error_code
        self._description = description
        self._error_uri = error_uri

        super().__init__(*args)

    @property
    def error_code(self) -> str:
        return self._error_code

    @property
    def description(self) -> str:
        return self._description

    @property
    def error_uri(self) -> str:
        return self._error_uri
