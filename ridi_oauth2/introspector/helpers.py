from typing import Dict

import jwt

from ridi_oauth2.introspector.dtos import AccessTokenInfo, JwtInfo
from ridi_oauth2.introspector.exceptions import InvalidJwtSignatureException, InvalidToken
from ridi_oauth2.introspector.jwt_introspector import JwtIntrospector


class JwtIntrospectHelper:
    @staticmethod
    def introspect(jwt_infos: Dict[str, JwtInfo], access_token: str) -> AccessTokenInfo:
        try:
            unverified_header = jwt.get_unverified_header(access_token)
        except jwt.InvalidTokenError:
            raise InvalidToken

        kid = unverified_header.get('kid')
        if not kid:
            raise InvalidJwtSignatureException

        jwt_info = jwt_infos.get(kid)
        if not jwt_info:
            raise InvalidJwtSignatureException

        introspector = JwtIntrospector(jwt_info=jwt_info, access_token=access_token)
        result = introspector.introspect()

        try:
            return AccessTokenInfo.from_dict(result)

        except KeyError:
            raise InvalidJwtSignatureException
