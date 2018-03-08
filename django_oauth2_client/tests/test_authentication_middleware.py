import json
import time
from unittest.mock import Mock

import jwt
import requests_mock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import TestCase

from django_oauth2_client.config import RidiOAuth2Config
from django_oauth2_client.middlewares import AuthenticationMiddleware
from django_oauth2_client.response import HttpUnauthorizedResponse
from oauth2_client.dtos import TokenData


class AuthenticationMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = AuthenticationMiddleware()

        self.valid_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }, key='dummy_jwt_secret').decode()

        self.loose_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) + 60 * 60,
        }, key='dummy_jwt_secret').decode()

        self.expire_token = jwt.encode(payload={
            'sub': 'testuser',
            'u_idx': 123123,
            'exp': int(time.time()) - 60 * 60,
            'client_id': 'asfeih29snv8as213i',
            'scope': 'all'
        }, key='dummy_jwt_secret').decode()

    def test_login_and_not_expire(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.valid_token,
        }

        response = self.middleware.process_request(request=request)

        self.assertIsNone(response)
        self.assertTrue(request.user.is_authenticated)
        self.assertIsInstance(request.user, get_user_model())
        self.assertEqual(request.user.u_idx, request.user.token_info.u_idx)

    def test_not_login(self):
        request = Mock()
        request.COOKIES = {
        }

        response = self.middleware.process_request(request=request)

        self.assertIsNone(response)
        self.assertFalse(request.user.is_authenticated)
        self.assertIsInstance(request.user, AnonymousUser)

    def test_login_and_expire(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.expire_token,
        }

        response = self.middleware.process_request(request=request)

        self.assertIsNone(response, HttpUnauthorizedResponse)
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)

    def test_login_and_loose_token(self):
        request = Mock()
        request.COOKIES = {
            RidiOAuth2Config.get_access_token_cookie_key(): self.loose_token,
        }

        response = self.middleware.process_request(request=request)

        self.assertIsNone(response, HttpUnauthorizedResponse)
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)

    def test_access_token_expire_and_refresh_available(self):
        with requests_mock.Mocker() as m:
            m.post(RidiOAuth2Config.get_auth_server_info().token_url, text=json.dumps({
                'access_token': self.valid_token,
                'token_type': 'Bearer',
                'expires_in': 3600,
                'refresh_token': 'tGzv3JOkF0XG5Qx2TlKWIA',
                'refresh_token_expires_in': 3600 * 7,
                'scope': 'all',
            }))

            request = Mock()
            request.COOKIES = {
                RidiOAuth2Config.get_access_token_cookie_key(): self.expire_token,
                RidiOAuth2Config.get_refresh_token_cookie_key(): 'dummy-refresh-token'
            }

            response = self.middleware.process_request(request=request)
            token = getattr(request, '_token', None)

            self.assertIsNone(response)
            self.assertIsNotNone(token)
            self.assertEqual(token.access_token.token, self.valid_token)
            self.assertEqual(token.access_token.expires_in, 3600)
            self.assertEqual(token.refresh_token.token, 'tGzv3JOkF0XG5Qx2TlKWIA')
            self.assertEqual(token.refresh_token.expires_in, 3600 * 7)
            self.assertEqual(token.token_type, 'Bearer')
            self.assertEqual(token.scope, 'all')

    def test_set_cookie_response(self):
        request = Mock()
        request._token = TokenData.from_dict(  # flake8: noqa: W0212  # pylint:disable=protected-access
            {'access_token': 'this_is_new_dummy_at', 'refresh_token': 'this_is_new_dummy_rt'}
        )
        response = HttpResponse()

        response = self.middleware.process_response(request=request, response=response)

        self.assertIn(RidiOAuth2Config.get_access_token_cookie_key(), response.cookies)
        self.assertIn(RidiOAuth2Config.get_refresh_token_cookie_key(), response.cookies)
