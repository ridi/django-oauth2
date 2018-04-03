import time
from unittest.mock import MagicMock, Mock

import jwt
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
        self.jwt_payload = {
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
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
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(payload=self.jwt_payload, key='dummy_jwt_secret').decode(),
        }
        self.middleware.process_request(request)

        del request.user.token_info

        response1 = self.dummy_view(None, request)

        self.assertIsNone(getattr(request.user, 'token_info', None))
        self.assertIsInstance(response1, HttpUnauthorizedResponse)
        self.assertEqual(response1.status_code, 401)

    def test_login(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(payload=self.jwt_payload, key='dummy_jwt_secret').decode(),
        }
        self.middleware.process_request(request)

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
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(payload=self.jwt_payload, key='dummy_jwt_secret').decode(),
        }
        self.middleware.process_request(request)

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
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(payload=self.jwt_loose_payload, key='dummy_jwt_secret').decode(),
        }
        self.middleware.process_request(request)

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
            RidiOAuth2Config.get_access_token_cookie_key(): jwt.encode(payload=self.jwt_loose_payload, key='dummy_jwt_secret').decode(),
        }
        self.middleware.process_request(request)

        response = self.dummy_view_with_custom_response(None, request)

        self.assertIn('user_info', request.user.token_info.scope)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content, b'tetete')
        self.assertEqual(response.status_code, 200)
