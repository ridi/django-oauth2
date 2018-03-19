import json
import unittest

import requests_mock

from ridi_oauth2.client.constants import OAuth2GrantType
from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.client.factory import OAuth2GrantFactory


class AuthorizationCodeGrantTestCase(unittest.TestCase):
    def setUp(self):
        self.client_info = ClientInfo(
            client_id='dummy_client_id', client_secret='dummy_client_secret', scope='all', redirect_uri='https://127.0.0.1:8000/callback'
        )
        self.auth_server_info = AuthorizationServerInfo(
            authorization_url='https://127.0.0.1/oauth2/authorize', token_url='https://127.0.0.1/oauth2/token'
        )
        self.grant_type = OAuth2GrantType.AUTHORIZATION_CODE

    def test_request_authorize(self):
        authorization_code_grant = OAuth2GrantFactory.get_grant(
            grant_type=self.grant_type, client_info=self.client_info, auth_server_info=self.auth_server_info
        )

        authorize_url, _ = authorization_code_grant.get_authorization_url()
        self.assertIn(self.auth_server_info.authorization_url, authorize_url)

    def test_get_token(self):
        authorization_code_grant = OAuth2GrantFactory.get_grant(
            grant_type=self.grant_type, client_info=self.client_info, auth_server_info=self.auth_server_info
        )
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

            result = authorization_code_grant.get_access_token(code=dummy_code)

            self.assertIsNotNone(result.access_token.token)
            self.assertIsNotNone(result.refresh_token.token)
            self.assertEqual(result.scope, self.client_info.scope)


class RefreshTokenGrantTestCase(unittest.TestCase):
    def setUp(self):
        self.client_info = ClientInfo(client_id='dummy_client_id', client_secret='dummy_client_secret', scope='all', )
        self.auth_server_info = AuthorizationServerInfo(token_url='https://127.0.0.1/oauth2/token')
        self.grant_type = OAuth2GrantType.REFRESH_TOKEN

    def test_not_implement_authorize(self):
        refresh_token_grant = OAuth2GrantFactory.get_grant(
            grant_type=self.grant_type, client_info=self.client_info, auth_server_info=self.auth_server_info
        )

        with self.assertRaises(NotImplementedError):
            refresh_token_grant.get_authorization_url()

    def test_get_token(self):
        refresh_token_grant = OAuth2GrantFactory.get_grant(
            grant_type=self.grant_type, client_info=self.client_info, auth_server_info=self.auth_server_info
        )

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

            result = refresh_token_grant.get_access_token(refresh_token=dummy_refresh_token)

            self.assertIsNotNone(result.access_token)
            self.assertIsNotNone(result.refresh_token)
            self.assertNotEqual(result.refresh_token, dummy_refresh_token)
            self.assertEqual(result.scope, self.client_info.scope)
