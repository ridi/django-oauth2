import typing
from base64 import urlsafe_b64decode
from datetime import datetime, timedelta

from Crypto.PublicKey import RSA

from lib.utils.bytes import bytes_to_int
from ridi_oauth2.introspector.constants import JWK_EXPIRES_MIN


class AccessTokenInfo:
    def __init__(self, subject: str, u_idx: int, expire: int, client_id: str, scope: typing.List):
        self._subject = subject
        self._u_idx = u_idx
        self._expire_timestamp = expire
        self._expire_date = datetime.fromtimestamp(expire)
        self._client_id = client_id
        self._scope = scope

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def u_idx(self) -> int:
        return self._u_idx

    @property
    def expire_timestamp(self) -> int:
        return self._expire_timestamp

    @property
    def expire_date(self) -> datetime:
        return self._expire_date

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def scope(self) -> typing.List:
        return self._scope

    @staticmethod
    def from_dict(dictionary: typing.Dict):
        return AccessTokenInfo(
            subject=dictionary['sub'], u_idx=dictionary['u_idx'], expire=dictionary['exp'], client_id=dictionary['client_id'],
            scope=dictionary['scope'],
        )


class JWKDto:
    def __init__(self, json):
        self._json = json
        self.expires = datetime.now() + timedelta(minutes=JWK_EXPIRES_MIN)
        decoded_n = bytes_to_int(urlsafe_b64decode(self.n))
        decoded_e = bytes_to_int(urlsafe_b64decode(self.e))
        self.public_key = RSA.construct((decoded_n, decoded_e)).exportKey().decode()

    @property
    def alg(self) -> str:
        return self._json.get('alg')

    @property
    def kty(self) -> str:
        return self._json.get('kty')

    @property
    def use(self) -> str:
        return self._json.get('use')

    @property
    def e(self) -> str:
        return self._json.get('e')

    @property
    def n(self) -> str:
        return self._json.get('n')

    @property
    def kid(self) -> str:
        return self._json.get('kid')

    @property
    def is_expired(self) -> bool:
        return self.expires < datetime.now()
