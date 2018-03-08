
import typing

import jwt

from oauth2_client.constants import TokenType
from oauth2_client.exceptions import ExpireTokenException, InvalidJwtSignatureException
from oauth2_client.introspetor.dtos import JwtInfo
from .base import BaseIntrospector


class JwtIntrospector(BaseIntrospector):
    def __init__(self, jwt_info: JwtInfo, access_token: str):
        self._jwt_info = jwt_info
        super().__init__(access_token=access_token, token_type_hint=TokenType.BEARER)

    def introspect(self) -> typing.Dict:
        try:
            payload = jwt.decode(
                jwt=self.access_token, key=self._jwt_info.secret, algorithms=[self._jwt_info.algorithm], leeway=self._jwt_info.expire_term
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpireTokenException
        except jwt.exceptions.DecodeError:
            raise InvalidJwtSignatureException

        return self._active_response(payload=payload)

    @staticmethod
    def _active_response(payload: typing.Dict) -> typing.Dict:
        payload.update({'active': True})
        return payload
