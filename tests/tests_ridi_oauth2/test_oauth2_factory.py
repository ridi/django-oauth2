import unittest

from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.client.exceptions import NotSupportedGrantException
from ridi_oauth2.client.factory import OAuth2GrantFactory
from ridi_oauth2.client.grant.authorization_code import AuthorizationCodeGrant
from ridi_oauth2.client.grant.base import BaseGrant
from ridi_oauth2.client.grant.refresh_token import RefreshTokenGrant
from ridi_oauth2.common.constants import OAuth2GrantType


class OAuth2FactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client_info = ClientInfo(client_id='123123', client_secret='asdfasdf')
        self.auth_server_info = AuthorizationServerInfo()

    def test_raise_not_support_grant(self):
        with self.assertRaises(NotSupportedGrantException):
            OAuth2GrantFactory.get_grant(
                grant_type=OAuth2GrantType.IMPLICIT, client_info=self.client_info, auth_server_info=self.auth_server_info
            )

        with self.assertRaises(NotSupportedGrantException):
            OAuth2GrantFactory.get_grant(
                grant_type='custom_grant', client_info=self.client_info, auth_server_info=self.auth_server_info
            )

    def test_get_grant(self):
        authorization_code_grant = OAuth2GrantFactory.get_grant(
            grant_type=OAuth2GrantType.AUTHORIZATION_CODE, client_info=self.client_info, auth_server_info=self.auth_server_info
        )
        refresh_token_grant = OAuth2GrantFactory.get_grant(
            grant_type=OAuth2GrantType.REFRESH_TOKEN, client_info=self.client_info, auth_server_info=self.auth_server_info
        )

        self.assertIsInstance(authorization_code_grant, BaseGrant)
        self.assertIsInstance(refresh_token_grant, BaseGrant)

        self.assertIsInstance(authorization_code_grant, AuthorizationCodeGrant)
        self.assertIsInstance(refresh_token_grant, RefreshTokenGrant)
