
DEFAULT_EXPIRE_TERM = 60 * 5  # second


class JwtInfo:
    def __init__(self, secret: str, algorithm: str, expire_term: int=DEFAULT_EXPIRE_TERM):
        self._secret = secret
        self._algorithm = algorithm
        self._expire_term = expire_term

    @property
    def secret(self) -> str:
        return self._secret

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @property
    def expire_term(self) -> int:
        return self._expire_term
