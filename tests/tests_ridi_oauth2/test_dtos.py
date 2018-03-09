import unittest

from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.introspetor.dtos import JwtInfo


class JwtInfoTestCase(unittest.TestCase):
    def test_jwt_info(self):
        secret = 'asdfasdfasdf'
        algorithm = 'HS256'

        jwt_info = JwtInfo(secret=secret, algorithm=algorithm)

        self.assertEqual(jwt_info.secret, secret)
        self.assertEqual(jwt_info.algorithm, algorithm)


class ClientInfoTestCase(unittest.TestCase):
    def test_full_client_info(self):
        client_id = 'arvnawrnf910#$#*R'
        client_secret = 'asdf#asd#*Rff'
        scope = 'all'
        redirect_uri = 'https://127.0.0.1/oauth2/callback/'

        client_info = ClientInfo(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)

        self.assertEqual(client_info.client_id, client_id)
        self.assertEqual(client_info.client_secret, client_secret)
        self.assertEqual(client_info.scope, scope)
        self.assertEqual(client_info.redirect_uri, redirect_uri)

    def test_loose_client_info(self):
        client_id = 'arvnawrnf910#$#*R'
        client_secret = 'asdf#asd#*Rff'

        client_info = ClientInfo(client_id=client_id, client_secret=client_secret)

        self.assertEqual(client_info.client_id, client_id)
        self.assertEqual(client_info.client_secret, client_secret)
        self.assertIsNone(client_info.scope)
        self.assertIsNone(client_info.redirect_uri)


class AuthorizationServerInfoTestCase(unittest.TestCase):
    def test_full_authorization_server_info(self):
        authorization_url = 'https://account.ridibooks.com/oauth2/authorize/'
        token_url = 'https://account.ridibooks.com/oauth2/token/'

        auth_server_info = AuthorizationServerInfo(authorization_url=authorization_url, token_url=token_url)

        self.assertEqual(auth_server_info.authorization_url, authorization_url)
        self.assertEqual(auth_server_info.token_url, token_url)

    def test_loose_authorization_server_info(self):
        token_url = 'https://account.ridibooks.com/oauth2/token/'

        auth_server_info = AuthorizationServerInfo(token_url=token_url)

        self.assertIsNone(auth_server_info.authorization_url)
        self.assertEqual(auth_server_info.token_url, token_url)

    def test_empty_authorization_server_info(self):
        auth_server_info = AuthorizationServerInfo()

        self.assertIsNone(auth_server_info.authorization_url)
        self.assertIsNone(auth_server_info.token_url)
