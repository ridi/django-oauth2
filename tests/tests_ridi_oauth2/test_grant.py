import json
import unittest

import requests_mock

from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.client.grant import Grant
from ridi_oauth2.common.utils.string import generate_random_str


class GrantTestCase(unittest.TestCase):
    def setUp(self):
        self.client_info = ClientInfo(
            client_id='dummy_client_id', client_secret='dummy_client_secret', scope='all', redirect_uri='https://127.0.0.1:8000/callback'
        )
        self.auth_server_info = AuthorizationServerInfo(
            authorization_url='https://127.0.0.1/oauth2/authorize', token_url='https://127.0.0.1/oauth2/token'
        )
        self.grant = Grant(client_info=self.client_info, auth_server_info=self.auth_server_info)

    def test_authorize(self):
        state = generate_random_str()
        authorize_url = self.grant.authorize(state=state)
        self.assertIn(self.auth_server_info.authorization_url, authorize_url)

    def test_code(self):
        dummy_code = 'this.is.dummy.code'

        with requests_mock.Mocker() as m:
            m.post(self.auth_server_info.token_url, text=json.dumps({
                'access_token': '2YotnFZFEjr1zCsicMWpAA',
                'token_type': 'bearer',
                'expires_in': 3600,
                'refresh_token': 'tGzv3JOkF0XG5Qx2TlKWIA',
                'refresh_token_expires_in': 3600 * 7,
                'scope': 'all',
            }))

            result = self.grant.code(code=dummy_code)

            self.assertIsNotNone(result.access_token.token)
            self.assertIsNotNone(result.refresh_token.token)
            self.assertEqual(result.scope, self.client_info.scope)

    def test_refresh(self):
        dummy_refresh_token = 'this.is.refresh.token.'

        with requests_mock.Mocker() as m:
            m.post(self.auth_server_info.token_url, text=json.dumps({
                'access_token': '2YotnFZFEjr1zCsicMWpAA',
                'token_type': 'bearer',
                'expires_in': 3600,
                'refresh_token': 'tGzv3JOkF0XG5Qx2TlKWIA',
                'refresh_token_expires_in': 3600 * 7,
                'scope': 'all',
            }))

            result = self.grant.refresh(refresh_token=dummy_refresh_token)

            self.assertIsNotNone(result.access_token)
            self.assertIsNotNone(result.refresh_token)
            self.assertNotEqual(result.refresh_token, dummy_refresh_token)
            self.assertEqual(result.scope, self.client_info.scope)
