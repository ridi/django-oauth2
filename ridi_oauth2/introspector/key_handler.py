from datetime import datetime, timedelta
from typing import Dict, List

import jwt
import requests
from Crypto.PublicKey import RSA
from requests import RequestException, Response

from lib.decorators.memorize import memorize
from lib.decorators.retry import RetryFailException, retry
from lib.utils.bytes import bytes_to_int
from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_oauth2.client.dtos import KeyAuthInfo
from ridi_oauth2.introspector.constants import JWKKeyType, JWKUse, JWK_EXPIRES_MIN
from ridi_oauth2.introspector.dtos import JWKDto
from ridi_oauth2.introspector.exceptions import AccountServerException, ClientRequestException, FailToLoadPublicKeyException, NotExistedKey, \
    InvalidPublicKey
from base64 import urlsafe_b64decode


class KeyHandler:
    _public_key_dtos = {}

    @classmethod
    def _get_memorized_key_dto(cls, client_id: str, kid: str) -> JWKDto:
        return cls._public_key_dtos.get(client_id, {}).get(kid, None)

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

            if public_key_dto.kty != JWKKeyType.RSA or public_key_dto.use != JWKUse.SIG:
                raise InvalidPublicKey

        return cls._get_public_pem(public_key_dto)

    @classmethod
    def _memorize_key_dtos(cls, client_id: str, keys: List[JWKDto]):
        key_dtos = cls._public_key_dtos.get(client_id, {})
        for key in keys:
            key_dtos[key.kid] = key
        cls._public_key_dtos[client_id] = key_dtos

    @staticmethod
    @memorize(60 * JWK_EXPIRES_MIN)
    def _get_public_pem(key: JWKDto) -> str:
        decoded_n = bytes_to_int(urlsafe_b64decode(key.n))
        decoded_e = bytes_to_int(urlsafe_b64decode(key.e))
        return RSA.construct((decoded_n, decoded_e)).exportKey().decode()

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
        if response.status_code >= 500:
            raise AccountServerException
        elif response.status_code >= 400:
            raise ClientRequestException
        return response.json()

    @classmethod
    @retry(retry_count=3, retriable_exceptions=(RequestException, AccountServerException,))
    def _get_valid_public_keys_by_client_id(cls, client_id: str) -> List[JWKDto]:
        internal_key_auth_info = RidiOAuth2Config.get_internal_key_auth_info()
        headers = {'Authorization': f'Bearer {cls._generate_internal_auth_token(internal_key_auth_info)}'}

        response = requests.request(
            method='GET',
            url=internal_key_auth_info.url,
            headers=headers,
            params={'client_id': client_id},
        )
        return [JWKDto(key) for key in cls._process_response(response=response).get('keys')]
