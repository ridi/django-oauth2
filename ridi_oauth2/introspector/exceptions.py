class InvalidJwtSignatureException(Exception):
    pass


class ExpireTokenException(Exception):
    pass


class InvalidToken(Exception):
    pass


class InvalidPublicKey(Exception):
    pass
