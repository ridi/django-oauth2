from ridi_oauth2.introspector.dtos import AccessTokenInfo, JwtInfo
from ridi_oauth2.introspector.exceptions import InvalidJwtSignatureException
from ridi_oauth2.introspector.jwt_introspector import JwtIntrospector


class JwtIntrospectHelper:
    @staticmethod
    def introspect(jwt_info: JwtInfo, access_token: str) -> AccessTokenInfo:
        introspector = JwtIntrospector(jwt_info=jwt_info, access_token=access_token)
        result = introspector.introspect()
        try:
            return AccessTokenInfo.from_dict(result)
        except KeyError:
            raise InvalidJwtSignatureException
