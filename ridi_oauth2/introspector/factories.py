from ridi_oauth2.introspector.constants import JWKKeyType
from ridi_oauth2.introspector.dtos import JWKRSADto, JWKECDto, BaseJWKDto


class JWKDtoFactory:
    @staticmethod
    def getDto(json) -> BaseJWKDto:
        kty = json.get('kty')
        if kty == JWKKeyType.RSA:
            return JWKRSADto(json)
        elif kty == JWKKeyType.EC:
            return JWKECDto(json)

        raise NotImplementedError
