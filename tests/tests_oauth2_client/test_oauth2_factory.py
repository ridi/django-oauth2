import unittest

from oauth2_client.constants import OAuth2GrantType
from oauth2_client.exceptions import NotSupportedGrantException
from oauth2_client.oauth2.dtos import AuthorizationServerInfo, ClientInfo
from oauth2_client.oauth2.factory import OAuth2GrantFactory
from oauth2_client.oauth2.grant.authorization_code import AuthorizationCodeGrant
from oauth2_client.oauth2.grant.base import BaseGrant
from oauth2_client.oauth2.grant.refresh_token import RefreshTokenGrant


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
