from typing import Dict, List

import requests
from requests import Response, HTTPError

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2_lib.decorators.retry import RetryFailException, retry
from ridi_oauth2.introspector.constants import JWKKeyType, JWKUse
from ridi_oauth2.introspector.dtos import BaseJWKDto
from ridi_oauth2.introspector.exceptions import FailToLoadPublicKeyException, \
    InvalidPublicKey, NotExistedKey
from ridi_oauth2.introspector.factories import JWKDtoFactory


class KeyHandler:
    _public_key_dtos = {}

    @classmethod
    def _get_memorized_key_dto(cls, client_id: str, kid: str) -> BaseJWKDto:
        return cls._public_key_dtos.get(client_id, {}).get(kid, None)

    @classmethod
    def get_public_key_by_kid(cls, client_id: str, kid: str):
        public_key_dto = cls._get_memorized_key_dto(client_id, kid)

        if not public_key_dto or public_key_dto.is_expired:
            public_key_dto = cls._reset_key_dtos(client_id, kid)

        cls._assert_valid_key(public_key_dto)

        return public_key_dto.public_key

    @staticmethod
    def _assert_valid_key(key: BaseJWKDto):
        if not key:
            raise NotExistedKey
        if key.kty not in (JWKKeyType.RSA, JWKKeyType.EC) or key.use != JWKUse.SIG:
            raise InvalidPublicKey

    @classmethod
    def _reset_key_dtos(cls, client_id: str, kid: str) -> BaseJWKDto:
        try:
            keys = cls._get_valid_public_keys_by_client_id(client_id)

        except RetryFailException as e:
            raise FailToLoadPublicKeyException from e

        cls._memorize_key_dtos(client_id, keys)

        return cls._get_memorized_key_dto(client_id, kid)

    @classmethod
    def _memorize_key_dtos(cls, client_id: str, keys: List[BaseJWKDto]):
        key_dtos = cls._public_key_dtos.get(client_id, {})
        for key in keys:
            key_dtos[key.kid] = key
        cls._public_key_dtos[client_id] = key_dtos

    @staticmethod
    def _process_response(response: Response) -> Dict:
        response.raise_for_status()
        return response.json()

    @classmethod
    @retry(retry_count=3, retriable_exceptions=(HTTPError, ))
    def _get_valid_public_keys_by_client_id(cls, client_id: str) -> List[BaseJWKDto]:
        response = requests.request(
            method='GET',
            url=RidiOAuth2Config.get_key_url(),
            params={'client_id': client_id},
        )
        return [JWKDtoFactory.get_dto(key) for key in cls._process_response(response=response).get('keys')]
