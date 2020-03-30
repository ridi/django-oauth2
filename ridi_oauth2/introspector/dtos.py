import typing
from base64 import urlsafe_b64decode
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers, SECP256R1
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from ridi_django_oauth2_lib.utils.bytes import bytes_to_int
from ridi_oauth2.introspector.constants import JWK_EXPIRES_MIN, JWKCrv


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


class BaseJWKDto:
    def __init__(self, json):
        self._json = json
        self.expires = datetime.now() + timedelta(minutes=JWK_EXPIRES_MIN)

    @property
    def kid(self) -> str:
        return self._json.get('kid')

    @property
    def kty(self) -> str:
        return self._json.get('kty')

    @property
    def use(self) -> str:
        return self._json.get('use')

    @property
    def alg(self) -> str:
        return self._json.get('alg')

    @property
    def is_expired(self) -> bool:
        return self.expires < datetime.now()


class JWKRSADto(BaseJWKDto):
    def __init__(self, json):
        super().__init__(json)
        decoded_n = bytes_to_int(urlsafe_b64decode(self.n))
        decoded_e = bytes_to_int(urlsafe_b64decode(self.e))
        rsa_public_key = RSAPublicNumbers(decoded_e, decoded_n).public_key(default_backend())
        self.public_key = rsa_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()

    @property
    def e(self) -> str:
        return self._json.get('e')

    @property
    def n(self) -> str:
        return self._json.get('n')


class JWKECDto(BaseJWKDto):
    def __init__(self, json):
        super().__init__(json)
        decoded_x = bytes_to_int(urlsafe_b64decode(self.x))
        decoded_y = bytes_to_int(urlsafe_b64decode(self.y))
        ec_public_key = EllipticCurvePublicNumbers(
            decoded_x,
            decoded_y,
            self._get_curve_instance()
        ).public_key(default_backend())
        self.public_key = ec_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()

    def _get_curve_instance(self):
        if self.crv == JWKCrv.P256:
            return SECP256R1()

        raise NotImplementedError

    @property
    def crv(self) -> str:
        return self._json.get('crv')

    @property
    def x(self) -> str:
        return self._json.get('x')

    @property
    def y(self) -> str:
        return self._json.get('y')
