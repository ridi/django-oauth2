import jwt
from jwt import InvalidTokenError
from jwt.exceptions import InvalidKeyError

from ridi_oauth2.introspector.dtos import AccessTokenInfo
from ridi_oauth2.introspector.exceptions import InvalidJwtSignatureException, InvalidToken
from ridi_oauth2.introspector.key_handler import KeyHandler


class JwtIntrospectHelper:
    @staticmethod
    def introspect(access_token: str) -> AccessTokenInfo:
        try:
            unverified_header = jwt.get_unverified_header(access_token)
            unverified_payload = jwt.decode(access_token, verify=False)
        except jwt.InvalidTokenError as e:
            raise InvalidToken from e

        kid = unverified_header.get('kid', None)
        client_id = unverified_payload.get('client_id', None)

        if not kid or not client_id:
            raise InvalidJwtSignatureException

        public_key = KeyHandler.get_public_key_by_kid(client_id, kid)

        try:
            payload = jwt.decode(jwt=access_token, key=public_key, algorithms=unverified_header.get('alg'))
            return AccessTokenInfo.from_dict(payload)
        except (InvalidTokenError, InvalidKeyError) as e:
            raise InvalidJwtSignatureException from e
