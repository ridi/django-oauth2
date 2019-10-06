from datetime import datetime, timedelta
from typing import Dict, List

import jwt
import requests
from requests import RequestException, Response

from lib.decorators.retry import RetryFailException, retry
from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_oauth2.client.dtos import KeyAuthInfo
from ridi_oauth2.introspector.dtos import KeyDto
from ridi_oauth2.introspector.exceptions import AccountServerException, ClientRequestException, FailToLoadPublicKeyException, NotExistedKey


class KeyHandler:
    _public_key_dtos = {}

    @classmethod
    def get_public_key_by_kid(cls, client_id: str, kid: str):
        public_key_dto = cls._get_memorized_key_dto(client_id, kid)

        if not public_key_dto or public_key_dto.is_expired:
            try:
                keys = cls._get_valid_public_keys_by_client_id(client_id)
                cls._memorize_key_dtos(client_id, keys)
            except RetryFailException:
                raise FailToLoadPublicKeyException

            public_key_dto = cls._get_memorized_key_dto(client_id, kid)

            if not public_key_dto:
                raise NotExistedKey

        return public_key_dto.public_key

    @classmethod
    def _get_memorized_key_dto(cls, client_id: str, kid: str) -> KeyDto:
        return cls._public_key_dtos.get(client_id, {}).get(kid, None)

    @classmethod
    def _memorize_key_dtos(cls, client_id: str, keys: List[KeyDto]):
        key_dtos = cls._public_key_dtos.get(client_id, {})
        for key in keys:
            key_dtos[key.kid] = key
        cls._public_key_dtos[client_id] = key_dtos

    @staticmethod
    def _generate_internal_auth_token(internal_key_auth_info: KeyAuthInfo) -> str:
        payload = {
            'iss': internal_key_auth_info.iss,
            'aud': internal_key_auth_info.aud,
            'exp': datetime.now() + timedelta(seconds=internal_key_auth_info.ttl_seconds)
        }
        return jwt.encode(payload, internal_key_auth_info.secret, algorithm=internal_key_auth_info.alg).decode()

    @staticmethod
    def _process_response(response: Response) -> Dict:
        if response.status_code > 499:
            raise AccountServerException
        elif response.status_code > 399:
            raise ClientRequestException
        return response.json()

    @classmethod
    @retry(retry_count=3, retriable_exceptions=(RequestException, AccountServerException,))
    def _get_valid_public_keys_by_client_id(cls, client_id: str) -> List[KeyDto]:
        internal_key_auth_info = RidiOAuth2Config.get_internal_key_auth_info()
        headers = {'Authorization': f'Bearer {cls._generate_internal_auth_token(internal_key_auth_info)}'}

        response = requests.request(
            method='GET',
            url=internal_key_auth_info.url,
            headers=headers,
            params={'client_id': client_id},
        )
        return [KeyDto(key) for key in cls._process_response(response=response).get('keys')]
