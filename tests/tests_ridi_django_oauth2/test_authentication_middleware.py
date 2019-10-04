import json
import time
from unittest.mock import Mock

import jwt
import requests_mock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2.middlewares import AuthenticationMiddleware
from ridi_django_oauth2.response import HttpUnauthorizedResponse


class AuthenticationMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = AuthenticationMiddleware()
        self.headers = {
            'kid': 'RS999',
        }
        self.private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEA1rL5PCEv2PaAASaGldzfnlo0MiMCglC+eFxYHgUfa6a7qJhj\no0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n\n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/FuplBFT82e14UVmZx4kP+HwDjaSp\nvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+EOuEBQ+QIIe5Npd49gzq4CGHeNJlP\nQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh\n5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQIDAQABAoIBAGxaiORqz04NIY7z\nFYs+nHC7j4oaFyMTgv0Vhbco2LGoxR6SQf7c18Q5qBKSznfp32HqLdj1nKpLxR7V\no/WSqqTPPLMU/oxI1TnFH8YUT918FbcbRNcSVsQirDWkpskpjoeMrBcGvE10u+aD\nJQnufKChDPhBuBZ3/Xf4415Lcw7xAsooHWxN5dBlq80ITyO3Rpwp7VayNRg3fzqy\ndZgsZoutyJmKd5dyKpckCpnGXOI1uvs/bnL2GLWWZvAS7/PDm+8pv3iVzmLB4J4J\njogLtJteHczxvVpIEotTAI7hLyb89k1NRncGE7zxKwtP0sIp1qg7AZGlVE8YImSg\nBhA4uU0CgYEA4uLFIx3td6jWstFok6/J36VHM8K/o8BqWgHqlypfwBAGMTuXwNHY\nMwFQNyTsT0BHoFN8e60s5wE1PxlL+hrjepXWxyCyWoHJqHpi3wqdDTMLkwniQnYr\n4c9cKcOAbkbVo+zsycuXiEQvXzLiltYII4P3KyBH4T+kQJM+4j8drocCgYEA8j/e\nXEJZaAAN95wUhfw1yfuJhXvZ5sB//nJlxCEnY3Kr5/o36eRTDGYai9qEkZEi2Ntz\nlB57mZQdI+VSRU5OADmQUYTVY5f+KQenzA0HnEFT/8aBdEvvGAWQDnULS4UPLqZS\nDUqV4L/CuBXhlHE7vz7nbNfQGzu+WG6EdJBb/xcCgYBwXjOYotfbbal3wrLyghuP\nQkIzZn6XUVLa5RwUZg4qB0Wp2IPeIY/cIwhhZ04KKiHPS8nZTvlwJ28Bozu30N1c\n9xz6Xj03ChSf9o1FPfJueRuAZWLD29b77UEOBh9zfm2M1GipwMV53ZtAoOkMH1DE\nljUyDLjM3EIzIToBv5SpvQKBgFSniRcIgKHdUwQyYOGpj0p0QkyJSU5f+tp6M6Hk\nTBVunzBDuoJbrcHpdGFnDWipJVpO5gbe2CaFIeHHY4agpJVjiFFUcBWLqd/AsxyV\neRFbqvT484gmePkWCI9ky3uqlfGhYY8Pf2y41lzqGJh9MXnVi533lNvPducER/lL\n8TolAoGANsr7iMbS5+iM6PvbSnkoNecVB2uScUO8K0ZIMNc2NDq1C+7tOGCQSi93\nIk7xlStrOD7vhmSSZuvUMZ23F7R9b8RXq0XIfokKYkPiCUjdrgC9PP54CDwUbglS\nlKP4SrbeuaTbTuMuuN6es7h1kkcz5qORtm1hWXLFTmloqYe4r5Q=\n-----END RSA PRIVATE KEY-----'
        self.public_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1rL5PCEv2PaAASaGldzf\nnlo0MiMCglC+eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3\nNIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/\nFuplBFT82e14UVmZx4kP+HwDjaSpvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+E\nOuEBQ+QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsB\nLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAn\nIQIDAQAB\n-----END PUBLIC KEY-----'

        self.valid_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }, key=self.private_key, algorithm='RS256', headers=self.headers).decode()

        self.loose_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
        }, key=self.private_key, algorithm='RS256', headers=self.headers).decode()

        self.expire_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) - 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }, key=self.private_key, algorithm='RS256', headers=self.headers).decode()

    def test_login_and_not_expire(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.valid_token,
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    'public_key': self.public_key,
                    'key_usage': 'generating_public_key',
                    'expires': '2099-12-31T10:00:00'
                }]
            }))

            response = self.middleware.process_request(request=request)

        self.assertIsNone(response)
        self.assertTrue(request.user.is_authenticated)
        self.assertIsInstance(request.user, get_user_model())
        self.assertEqual(request.user.u_idx, request.user.token_info.u_idx)

    def test_not_login(self):
        request = Mock()
        request.COOKIES = {
        }

        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    'public_key': self.public_key,
                    'key_usage': 'generating_public_key',
                    'expires': '2099-12-31T10:00:00'
                }]
            }))

            response = self.middleware.process_request(request=request)

        self.assertIsNone(response)
        self.assertFalse(request.user.is_authenticated)
        self.assertIsInstance(request.user, AnonymousUser)

    def test_login_and_expire(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.expire_token,
        }

        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    'public_key': self.public_key,
                    'key_usage': 'generating_public_key',
                    'expires': '2099-12-31T10:00:00'
                }]
            }))

            response = self.middleware.process_request(request=request)

        self.assertIsNone(response, HttpUnauthorizedResponse)
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)

    def test_login_and_loose_token(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.loose_token,
        }

        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    'public_key': self.public_key,
                    'key_usage': 'generating_public_key',
                    'expires': '2099-12-31T10:00:00'
                }]
            }))

            response = self.middleware.process_request(request=request)

        self.assertIsNone(response, HttpUnauthorizedResponse)
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
