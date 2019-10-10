import json
import time
from unittest.mock import MagicMock, Mock

import jwt
import requests_mock
from django.http import HttpResponse, HttpResponseForbidden
from django.test import TestCase

from ridi_django_oauth2.config import RidiOAuth2Config
from ridi_django_oauth2.decorators import login_required, scope_required
from ridi_django_oauth2.middlewares import AuthenticationMiddleware
from ridi_django_oauth2.response import HttpUnauthorizedResponse


def response_handler(request, *args, **kwargs) -> HttpResponse:
    return HttpResponse(content='tetete')


class LoginRequireTestCase(TestCase):
    def setUp(self):
        self.middleware = AuthenticationMiddleware()
        self.private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEA1rL5PCEv2PaAASaGldzfnlo0MiMCglC+eFxYHgUfa6a7qJhj\no0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n\n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/FuplBFT82e14UVmZx4kP+HwDjaSp\nvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+EOuEBQ+QIIe5Npd49gzq4CGHeNJlP\nQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh\n5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQIDAQABAoIBAGxaiORqz04NIY7z\nFYs+nHC7j4oaFyMTgv0Vhbco2LGoxR6SQf7c18Q5qBKSznfp32HqLdj1nKpLxR7V\no/WSqqTPPLMU/oxI1TnFH8YUT918FbcbRNcSVsQirDWkpskpjoeMrBcGvE10u+aD\nJQnufKChDPhBuBZ3/Xf4415Lcw7xAsooHWxN5dBlq80ITyO3Rpwp7VayNRg3fzqy\ndZgsZoutyJmKd5dyKpckCpnGXOI1uvs/bnL2GLWWZvAS7/PDm+8pv3iVzmLB4J4J\njogLtJteHczxvVpIEotTAI7hLyb89k1NRncGE7zxKwtP0sIp1qg7AZGlVE8YImSg\nBhA4uU0CgYEA4uLFIx3td6jWstFok6/J36VHM8K/o8BqWgHqlypfwBAGMTuXwNHY\nMwFQNyTsT0BHoFN8e60s5wE1PxlL+hrjepXWxyCyWoHJqHpi3wqdDTMLkwniQnYr\n4c9cKcOAbkbVo+zsycuXiEQvXzLiltYII4P3KyBH4T+kQJM+4j8drocCgYEA8j/e\nXEJZaAAN95wUhfw1yfuJhXvZ5sB//nJlxCEnY3Kr5/o36eRTDGYai9qEkZEi2Ntz\nlB57mZQdI+VSRU5OADmQUYTVY5f+KQenzA0HnEFT/8aBdEvvGAWQDnULS4UPLqZS\nDUqV4L/CuBXhlHE7vz7nbNfQGzu+WG6EdJBb/xcCgYBwXjOYotfbbal3wrLyghuP\nQkIzZn6XUVLa5RwUZg4qB0Wp2IPeIY/cIwhhZ04KKiHPS8nZTvlwJ28Bozu30N1c\n9xz6Xj03ChSf9o1FPfJueRuAZWLD29b77UEOBh9zfm2M1GipwMV53ZtAoOkMH1DE\nljUyDLjM3EIzIToBv5SpvQKBgFSniRcIgKHdUwQyYOGpj0p0QkyJSU5f+tp6M6Hk\nTBVunzBDuoJbrcHpdGFnDWipJVpO5gbe2CaFIeHHY4agpJVjiFFUcBWLqd/AsxyV\neRFbqvT484gmePkWCI9ky3uqlfGhYY8Pf2y41lzqGJh9MXnVi533lNvPducER/lL\n8TolAoGANsr7iMbS5+iM6PvbSnkoNecVB2uScUO8K0ZIMNc2NDq1C+7tOGCQSi93\nIk7xlStrOD7vhmSSZuvUMZ23F7R9b8RXq0XIfokKYkPiCUjdrgC9PP54CDwUbglS\nlKP4SrbeuaTbTuMuuN6es7h1kkcz5qORtm1hWXLFTmloqYe4r5Q=\n-----END RSA PRIVATE KEY-----'

        self.jwt_payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }

        self.headers = {
            'kid': 'RS999',
        }

        self.dummy_view = login_required()(MagicMock(return_value=HttpResponse(content='success')))
        self.custom_dummy_view = login_required(response_handler=response_handler)(MagicMock(return_value=HttpResponse(content='success')))

    def test_not_login(self):
        request = Mock()
        request.COOKIES = {}
        self.middleware.process_request(request)

        response = self.dummy_view(None, request)
        self.assertIsInstance(response, HttpUnauthorizedResponse)
        self.assertEqual(response.status_code, 401)

    def test_not_login_with_custom_response(self):
        request = Mock()
        request.COOKIES = {}
        self.middleware.process_request(request)

        response = self.custom_dummy_view(None, request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content, b'tetete')
        self.assertEqual(response.status_code, 200)

    def test_not_exists_token_info(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(
                self.jwt_payload, key=self.private_key, algorithm='RS256', headers=self.headers
            ).decode(),
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            self.middleware.process_request(request=request)
            del request.user.token_info

            response1 = self.dummy_view(None, request)

        self.assertIsNone(getattr(request.user, 'token_info', None))
        self.assertIsInstance(response1, HttpUnauthorizedResponse)
        self.assertEqual(response1.status_code, 401)

    def test_login(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(
                self.jwt_payload, key=self.private_key, algorithm='RS256', headers=self.headers
            ).decode(),
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            self.middleware.process_request(request=request)
        response = self.dummy_view(None, request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'success')


class ScopeRequireTestCase(TestCase):
    def setUp(self):
        self.middleware = AuthenticationMiddleware()
        self.jwt_payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }

        self.jwt_loose_payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'user_info'
        }

        self.headers = {
            'kid': 'RS999',
        }
        self.private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEA1rL5PCEv2PaAASaGldzfnlo0MiMCglC+eFxYHgUfa6a7qJhj\no0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n\n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/FuplBFT82e14UVmZx4kP+HwDjaSp\nvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+EOuEBQ+QIIe5Npd49gzq4CGHeNJlP\nQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh\n5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQIDAQABAoIBAGxaiORqz04NIY7z\nFYs+nHC7j4oaFyMTgv0Vhbco2LGoxR6SQf7c18Q5qBKSznfp32HqLdj1nKpLxR7V\no/WSqqTPPLMU/oxI1TnFH8YUT918FbcbRNcSVsQirDWkpskpjoeMrBcGvE10u+aD\nJQnufKChDPhBuBZ3/Xf4415Lcw7xAsooHWxN5dBlq80ITyO3Rpwp7VayNRg3fzqy\ndZgsZoutyJmKd5dyKpckCpnGXOI1uvs/bnL2GLWWZvAS7/PDm+8pv3iVzmLB4J4J\njogLtJteHczxvVpIEotTAI7hLyb89k1NRncGE7zxKwtP0sIp1qg7AZGlVE8YImSg\nBhA4uU0CgYEA4uLFIx3td6jWstFok6/J36VHM8K/o8BqWgHqlypfwBAGMTuXwNHY\nMwFQNyTsT0BHoFN8e60s5wE1PxlL+hrjepXWxyCyWoHJqHpi3wqdDTMLkwniQnYr\n4c9cKcOAbkbVo+zsycuXiEQvXzLiltYII4P3KyBH4T+kQJM+4j8drocCgYEA8j/e\nXEJZaAAN95wUhfw1yfuJhXvZ5sB//nJlxCEnY3Kr5/o36eRTDGYai9qEkZEi2Ntz\nlB57mZQdI+VSRU5OADmQUYTVY5f+KQenzA0HnEFT/8aBdEvvGAWQDnULS4UPLqZS\nDUqV4L/CuBXhlHE7vz7nbNfQGzu+WG6EdJBb/xcCgYBwXjOYotfbbal3wrLyghuP\nQkIzZn6XUVLa5RwUZg4qB0Wp2IPeIY/cIwhhZ04KKiHPS8nZTvlwJ28Bozu30N1c\n9xz6Xj03ChSf9o1FPfJueRuAZWLD29b77UEOBh9zfm2M1GipwMV53ZtAoOkMH1DE\nljUyDLjM3EIzIToBv5SpvQKBgFSniRcIgKHdUwQyYOGpj0p0QkyJSU5f+tp6M6Hk\nTBVunzBDuoJbrcHpdGFnDWipJVpO5gbe2CaFIeHHY4agpJVjiFFUcBWLqd/AsxyV\neRFbqvT484gmePkWCI9ky3uqlfGhYY8Pf2y41lzqGJh9MXnVi533lNvPducER/lL\n8TolAoGANsr7iMbS5+iM6PvbSnkoNecVB2uScUO8K0ZIMNc2NDq1C+7tOGCQSi93\nIk7xlStrOD7vhmSSZuvUMZ23F7R9b8RXq0XIfokKYkPiCUjdrgC9PP54CDwUbglS\nlKP4SrbeuaTbTuMuuN6es7h1kkcz5qORtm1hWXLFTmloqYe4r5Q=\n-----END RSA PRIVATE KEY-----'

        self.dummy_view1 = scope_required(required_scopes=['user_info'])(MagicMock(return_value=HttpResponse(content='success1')))
        self.dummy_view2 = scope_required(required_scopes=[('user_info', 'purchase')])(
            MagicMock(return_value=HttpResponse(content='success2'))
        )
        self.dummy_view_with_custom_response = scope_required(
            required_scopes=[('user_info', 'purchase')], response_handler=response_handler
        )(MagicMock(return_value=HttpResponse(content='success2')))

    def test_all_scope(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(
                self.jwt_payload, self.private_key, algorithm='RS256', headers=self.headers
            ).decode(),
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            self.middleware.process_request(request=request)

        response1 = self.dummy_view1(None, request)
        response2 = self.dummy_view2(None, request)

        self.assertIn('all', request.user.token_info.scope)

        self.assertIsInstance(response1, HttpResponse)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.content.decode(), 'success1')

        self.assertIsInstance(response2, HttpResponse)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.content.decode(), 'success2')

    def test_restriction_scope(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(
                self.jwt_loose_payload, self.private_key, algorithm='RS256', headers=self.headers
            ).decode(),
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            self.middleware.process_request(request=request)

        response1 = self.dummy_view1(None, request)
        response2 = self.dummy_view2(None, request)

        self.assertIn('user_info', request.user.token_info.scope)

        self.assertIsInstance(response1, HttpResponse)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.content.decode(), 'success1')

        self.assertIsInstance(response2, HttpResponseForbidden)
        self.assertEqual(response2.status_code, 403)

    def test_restriction_scope_with_custom_response(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(
                self.jwt_loose_payload, self.private_key, algorithm='RS256', headers=self.headers
            ).decode(),
        }
        with requests_mock.Mocker() as m:
            m.get(RidiOAuth2Config.get_internal_key_auth_info().url, text=json.dumps({
                'keys': [{
                    'kid': 'RS999',
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": "1rL5PCEv2PaAASaGldzfnlo0MiMCglC-eFxYHgUfa6a7qJhjo0QX8LeAelBlQpMCAMVGX33jUJ2FCCP_QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg_FuplBFT82e14UVmZx4kP-HwDjaSpvYHoTr3b5j20Ebx7aIy_SVrWeY0wxeAdFf-EOuEBQ-QIIe5Npd49gzq4CGHeNJlPQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQ==",
                    "e": "AQAB",
                }]
            }))

            self.middleware.process_request(request=request)

        response = self.dummy_view_with_custom_response(None, request)

        self.assertIn('user_info', request.user.token_info.scope)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content, b'tetete')
        self.assertEqual(response.status_code, 200)
