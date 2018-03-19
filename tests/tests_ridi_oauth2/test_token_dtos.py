import unittest
from datetime import datetime

from ridi_oauth2.client.dtos import TokenData
from ridi_oauth2.introspector.dtos import AccessTokenInfo

class TokenTestCase(unittest.TestCase):
    def setUp(self):
        self.simple_token_dict = {
            'access_token': 'test-access-token',
            'refresh_token': 'test-refresh-token',
        }

        self.full_token_dict = {
            'access_token': 'test-access-token',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': 'all',
            'refresh_token': 'test-refresh-token',
        }

    def test_simple_token(self):
        token = TokenData.from_dict(dictionary=self.simple_token_dict)

        self.assertEqual(token.access_token.token, self.simple_token_dict['access_token'])
        self.assertEqual(token.refresh_token.token, self.simple_token_dict['refresh_token'])
        self.assertIsNone(token.token_type)
        self.assertIsNone(token.scope)

    def test_full_token(self):
        token = TokenData.from_dict(dictionary=self.full_token_dict)

        self.assertEqual(token.access_token.token, self.full_token_dict['access_token'])
        self.assertEqual(token.refresh_token.token, self.full_token_dict['refresh_token'])
        self.assertEqual(token.token_type, self.full_token_dict['token_type'])
        self.assertEqual(token.scope, self.full_token_dict['scope'])


class TokenInfoTestCase(unittest.TestCase):
    def setUp(self):
        self.token_dict = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': 1555555555,
            'client_id': 'dummy_client_id',
            'scope': 'all',
        }

        self.loose_token_dict = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': 1555555555,
            'client_id': 'dummy_client_id',
        }

    def test_token_info_from_dict(self):
        token_info = AccessTokenInfo.from_dict(dictionary=self.token_dict)

        self.assertEqual(token_info.subject, self.token_dict['sub'])
        self.assertEqual(token_info.u_idx, self.token_dict['u_idx'])
        self.assertEqual(token_info.expire_timestamp, self.token_dict['exp'])
        self.assertEqual(token_info.expire_date, datetime.fromtimestamp(self.token_dict['exp']))
        self.assertEqual(token_info.client_id, self.token_dict['client_id'])
        self.assertEqual(token_info.scope, self.token_dict['scope'])

    def test_key_error(self):
        with self.assertRaises(KeyError):
            AccessTokenInfo.from_dict({})
