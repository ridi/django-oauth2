from datetime import datetime, timedelta
from typing import Dict, List

import jwt
import requests
from requests import RequestException, Response

from lib.decorators.retry import retry
from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_oauth2.client.dtos import KeyAuthInfo
from ridi_oauth2.introspector.dtos import KeyDto
from ridi_oauth2.introspector.exceptions import InvalidPublicKey


class KeyApiHelper:
    _public_key_dtos = {}

    @classmethod
    @retry(retry_count=3, retriable_exceptions=(InvalidPublicKey,))
    def get_public_key_by_kid(cls, client_id: str, kid: str):

        public_key_dto = cls._public_key_dtos.get(kid, None)

        if not public_key_dto or public_key_dto.is_expired:
            keys = cls._get_valid_public_keys_by_client_id(client_id)
            for key in keys:
                cls._public_key_dtos.setdefault(key.get('kid'), KeyDto(key))

            public_key_dto = cls._public_key_dtos.get(kid, None)

            if not public_key_dto:
                raise InvalidPublicKey

        return public_key_dto.public_key

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
        response.raise_for_status()
        return response.json()

    @classmethod
    def _get_valid_public_keys_by_client_id(cls, client_id: str) -> List[Dict]:
        internal_key_auth_info = RidiOAuth2Config.get_internal_key_auth_info()
        headers = {'Authorization': f'Bearer {cls._generate_internal_auth_token(internal_key_auth_info)}'}

        try:
            response = requests.request(
                method='GET',
                url=internal_key_auth_info.url,
                headers=headers,
                params={'client_id': client_id},
            )
            return cls._process_response(response=response).get('keys')
        except RequestException:
            raise InvalidPublicKey
