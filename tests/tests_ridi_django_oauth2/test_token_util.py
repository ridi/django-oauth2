import json
import time
from base64 import urlsafe_b64encode
from unittest.mock import Mock

import jwt
import requests_mock
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.utils import int_to_bytes
from django.test import TestCase

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2.utils.token import get_token_from_cookie, get_token_info


def generate_ec_private_key():
    return ec.generate_private_key(
        curve=ec.SECP256R1,
        backend=default_backend()
    )


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

    def test_token_info_by_rsa(self):
        payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }
        headers = {
            'kid': 'RS999',
        }
        private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEA1rL5PCEv2PaAASaGldzfnlo0MiMCglC+eFxYHgUfa6a7qJhj\no0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n\n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/FuplBFT82e14UVmZx4kP+HwDjaSp\nvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+EOuEBQ+QIIe5Npd49gzq4CGHeNJlP\nQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh\n5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQIDAQABAoIBAGxaiORqz04NIY7z\nFYs+nHC7j4oaFyMTgv0Vhbco2LGoxR6SQf7c18Q5qBKSznfp32HqLdj1nKpLxR7V\no/WSqqTPPLMU/oxI1TnFH8YUT918FbcbRNcSVsQirDWkpskpjoeMrBcGvE10u+aD\nJQnufKChDPhBuBZ3/Xf4415Lcw7xAsooHWxN5dBlq80ITyO3Rpwp7VayNRg3fzqy\ndZgsZoutyJmKd5dyKpckCpnGXOI1uvs/bnL2GLWWZvAS7/PDm+8pv3iVzmLB4J4J\njogLtJteHczxvVpIEotTAI7hLyb89k1NRncGE7zxKwtP0sIp1qg7AZGlVE8YImSg\nBhA4uU0CgYEA4uLFIx3td6jWstFok6/J36VHM8K/o8BqWgHqlypfwBAGMTuXwNHY\nMwFQNyTsT0BHoFN8e60s5wE1PxlL+hrjepXWxyCyWoHJqHpi3wqdDTMLkwniQnYr\n4c9cKcOAbkbVo+zsycuXiEQvXzLiltYII4P3KyBH4T+kQJM+4j8drocCgYEA8j/e\nXEJZaAAN95wUhfw1yfuJhXvZ5sB//nJlxCEnY3Kr5/o36eRTDGYai9qEkZEi2Ntz\nlB57mZQdI+VSRU5OADmQUYTVY5f+KQenzA0HnEFT/8aBdEvvGAWQDnULS4UPLqZS\nDUqV4L/CuBXhlHE7vz7nbNfQGzu+WG6EdJBb/xcCgYBwXjOYotfbbal3wrLyghuP\nQkIzZn6XUVLa5RwUZg4qB0Wp2IPeIY/cIwhhZ04KKiHPS8nZTvlwJ28Bozu30N1c\n9xz6Xj03ChSf9o1FPfJueRuAZWLD29b77UEOBh9zfm2M1GipwMV53ZtAoOkMH1DE\nljUyDLjM3EIzIToBv5SpvQKBgFSniRcIgKHdUwQyYOGpj0p0QkyJSU5f+tp6M6Hk\nTBVunzBDuoJbrcHpdGFnDWipJVpO5gbe2CaFIeHHY4agpJVjiFFUcBWLqd/AsxyV\neRFbqvT484gmePkWCI9ky3uqlfGhYY8Pf2y41lzqGJh9MXnVi533lNvPducER/lL\n8TolAoGANsr7iMbS5+iM6PvbSnkoNecVB2uScUO8K0ZIMNc2NDq1C+7tOGCQSi93\nIk7xlStrOD7vhmSSZuvUMZ23F7R9b8RXq0XIfokKYkPiCUjdrgC9PP54CDwUbglS\nlKP4SrbeuaTbTuMuuN6es7h1kkcz5qORtm1hWXLFTmloqYe4r5Q=\n-----END RSA PRIVATE KEY-----'

        valid_token = jwt.encode(payload=payload, key=private_key, algorithm='RS256', headers=headers).decode()

        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_key_url(), text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            token_info = get_token_info(token=valid_token)

        self.assertEqual(token_info.subject, payload['sub'])
        self.assertEqual(token_info.u_idx, payload['u_idx'])
        self.assertEqual(token_info.expire_timestamp, payload['exp'])
        self.assertEqual(token_info.client_id, payload['client_id'])
        self.assertIn(payload['scope'], token_info.scope)

    def test_token_info_by_ec(self):
        ec_key = generate_ec_private_key()

        public_numbers = ec_key.public_key().public_numbers()
        x = urlsafe_b64encode(int_to_bytes(public_numbers.x)).decode()
        y = urlsafe_b64encode(int_to_bytes(public_numbers.y)).decode()

        private_key = ec_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }
        headers = {
            'kid': 'ES999',
        }

        valid_token = jwt.encode(payload=payload, key=private_key, algorithm='ES256', headers=headers).decode()

        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_key_url(), text=json.dumps({
                'keys': [{
                    "kty": "EC",
                    "use": "sig",
                    "crv": "P-256",
                    "kid": "ES999",
                    "x": x,
                    "y": y,
                    "alg": "ES256"
                }]
            }))

            token_info = get_token_info(token=valid_token)

        self.assertEqual(token_info.subject, payload['sub'])
        self.assertEqual(token_info.u_idx, payload['u_idx'])
        self.assertEqual(token_info.expire_timestamp, payload['exp'])
        self.assertEqual(token_info.client_id, payload['client_id'])
        self.assertIn(payload['scope'], token_info.scope)
