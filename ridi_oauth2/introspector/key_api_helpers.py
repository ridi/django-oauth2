from datetime import datetime, timedelta
from http.client import HTTPException
from json import JSONDecodeError
from typing import Dict

import jwt
import requests
from requests import HTTPError, RequestException, Response

from ridi_oauth2.client.dtos import KeyAuthInfo
from ridi_oauth2.client.exceptions import InvalidResponseException, ServerException
from ridi_oauth2.introspector.dtos import KeyDto


class KeyApiHelper:
    _public_key_dtos = {}

    @classmethod
    def get_public_key_by_kid(cls, internal_key_auth_info: KeyAuthInfo, kid: str):
        public_key_dto = cls._public_key_dtos.get(kid, None)
        if not public_key_dto or public_key_dto.is_expired:
            cls._set_public_key_dtos_by_client_id(internal_key_auth_info)
            public_key_dto = cls._public_key_dtos.get(kid, None)
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
        try:
            response.raise_for_status()
            return response.json()

        except HTTPError as e:
            raise HTTPException(origin_exception=e, content=e.response.content, status=e.response.status_code)

        except (JSONDecodeError, TypeError):
            raise InvalidResponseException(response.content)

    @classmethod
    def _set_public_key_dtos_by_client_id(cls, internal_key_auth_info: KeyAuthInfo):
        headers = {
            'Authorization': f'Bearer {cls._generate_internal_auth_token(internal_key_auth_info)}'
        }
        try:
            response = requests.request(
                method='GET',
                url=internal_key_auth_info.url,
                headers=headers,
                params={'client_id': internal_key_auth_info.client_id},
                verify=False
            )

        except RequestException:
            raise ServerException

        for key in cls._process_response(response=response).get('keys'):
            cls._public_key_dtos.setdefault(key.get('kid'), KeyDto(key))
