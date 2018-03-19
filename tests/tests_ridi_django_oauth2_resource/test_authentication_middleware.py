import time
from unittest.mock import Mock

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from ridi_django_oauth2_resource.config import RidiOAuth2Config
from ridi_django_oauth2_resource.middlewares import AuthenticationMiddleware
from ridi_django_oauth2_resource.response import HttpUnauthorizedResponse


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
