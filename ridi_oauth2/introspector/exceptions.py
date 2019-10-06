class InvalidJwtSignatureException(Exception):
    pass


class ExpireTokenException(Exception):
    pass


class InvalidToken(Exception):
    pass


class PublicKeyException(Exception):
    pass


class FailToLoadPublicKeyException(PublicKeyException):
    pass


class NotExistedKey(PublicKeyException):
    pass


class PublicRequestException(PublicKeyException):
    pass


class AccountServerException(PublicRequestException):
    pass


class ClientRequestException(PublicRequestException):
    pass
