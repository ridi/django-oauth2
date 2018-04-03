import time
from unittest.mock import Mock

import jwt
from django.test import TestCase

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2.utils.token import get_token_from_cookie, get_token_info


class TokenUtilTestCase(TestCase):
    def test_token_from_cookie(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): 'this-is-access-token',
            RidiOAuth2Config.get_refresh_token_cookie_key(): 'this-is-refresh-token'
        }

        token = get_token_from_cookie(request=request)

        self.assertEqual(token.access_token.token, 'this-is-access-token')
        self.assertEqual(token.refresh_token.token, 'this-is-refresh-token')

    def test_token_info(self):
        payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }
        valid_token = jwt.encode(payload=payload, key='dummy_jwt_secret').decode()

        token_info = get_token_info(token=valid_token)

        self.assertEqual(token_info.subject, payload['sub'])
        self.assertEqual(token_info.u_idx, payload['u_idx'])
        self.assertEqual(token_info.expire_timestamp, payload['exp'])
        self.assertEqual(token_info.client_id, payload['client_id'])
        self.assertIn(payload['scope'], token_info.scope)
