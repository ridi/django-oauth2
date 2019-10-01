import jwt
from jwt import InvalidTokenError
from jwt.exceptions import InvalidKeyError

from ridi_oauth2.client.dtos import KeyAuthInfo
from ridi_oauth2.introspector.dtos import AccessTokenInfo
from ridi_oauth2.introspector.exceptions import InvalidJwtSignatureException, InvalidToken
from ridi_oauth2.introspector.key_api_helpers import KeyApiHelper


class JwtIntrospectHelper:
    @staticmethod
    def introspect(internal_key_auth_info: KeyAuthInfo, access_token: str) -> AccessTokenInfo:
        try:
            unverified_header = jwt.get_unverified_header(access_token)
        except jwt.InvalidTokenError:
            raise InvalidToken

        kid = unverified_header.get('kid')
        if not kid:
            raise InvalidJwtSignatureException

        public_key = KeyApiHelper.get_public_key_by_kid(internal_key_auth_info, kid)
        if not public_key:
            raise InvalidJwtSignatureException
        try:
            return jwt.decode(jwt=access_token, key=public_key, algorithms=unverified_header.get('alg'))
        except [InvalidTokenError, InvalidKeyError]:
            raise InvalidJwtSignatureException
