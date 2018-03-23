
import typing

import jwt

from ridi_oauth2.common.constants import TokenType
from ridi_oauth2.introspector.dtos import JwtInfo
from ridi_oauth2.introspector.exceptions import ExpireTokenException, InvalidJwtSignatureException
from .base import BaseIntrospector


class JwtIntrospector(BaseIntrospector):
    _DEFAULT_SCOPE_DELIMITER = ' '

    def __init__(self, jwt_info: JwtInfo, access_token: str):
        self._jwt_info = jwt_info
        super().__init__(access_token=access_token, token_type_hint=TokenType.BEARER)

    def introspect(self) -> typing.Dict:
        try:
            payload = jwt.decode(jwt=self.access_token, key=self._jwt_info.secret, algorithms=[self._jwt_info.algorithm])
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpireTokenException
        except jwt.exceptions.DecodeError:
            raise InvalidJwtSignatureException
        except jwt.InvalidAlgorithmError:
            raise InvalidJwtSignatureException

        payload = self._active_response(payload=payload)
        payload = self._split_scopes(payload=payload)
        return payload

    @staticmethod
    def _active_response(payload: typing.Dict) -> typing.Dict:
        payload.update({'active': True})
        return payload

    @classmethod
    def _split_scopes(cls, payload: typing.Dict) -> typing.Dict:
        if payload.get('scope', None) is None:
            return payload

        if isinstance(payload['scope'], list):
            return payload

        payload['scope'] = payload['scope'].split(cls._DEFAULT_SCOPE_DELIMITER)
        return payload
