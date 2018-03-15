import string
import time
import unittest

import jwt

from ridi_oauth2.common.utils.string import generate_random_str
from ridi_oauth2.introspector.dtos import JwtInfo
from ridi_oauth2.introspector.exceptions import ExpireTokenException, InvalidJwtSignatureException
from ridi_oauth2.introspector.jwt_introspector import JwtIntrospector


class JwtIntrospectorTestCase(unittest.TestCase):
    def setUp(self):
        self.secret = generate_random_str(chars=string.ascii_letters + string.digits + string.punctuation)
        self.alg = 'HS256'

        self.claim = {
            "sub": "testuser",
            "exp": int(time.time()) + 60 * 60,
        }
        self.token = jwt.encode(self.claim, self.secret, algorithm=self.alg)

        self.invalid_claim = {
            "sub": "testuser",
            "exp": int(time.time()) - 60 * 60,
        }
        self.invalid_token = jwt.encode(self.invalid_claim, self.secret, algorithm=self.alg)

    def test_introspect(self):
        jwt_info = JwtInfo(secret=self.secret, algorithm=self.alg)
        introspector = JwtIntrospector(jwt_info=jwt_info, access_token=self.token)

        result = introspector.introspect()
        _active = result.pop('active')

        self.assertTrue(_active)
        self.assertDictEqual(result, self.claim)

    def test_introspect_with_not_jwt_token(self):
        jwt_info = JwtInfo(secret=self.secret, algorithm=self.alg)
        introspector = JwtIntrospector(jwt_info=jwt_info, access_token="asdfasdfasdfasdf")

        with self.assertRaises(InvalidJwtSignatureException):
            introspector.introspect()

    def test_introspect_with_another_secret(self):
        jwt_info = JwtInfo(secret='asdfasdf', algorithm=self.alg)
        introspector = JwtIntrospector(jwt_info=jwt_info, access_token=self.token)

        with self.assertRaises(InvalidJwtSignatureException):
            introspector.introspect()

    def test_expire_token(self):
        jwt_info = JwtInfo(secret=self.secret, algorithm=self.alg)
        introspector = JwtIntrospector(jwt_info=jwt_info, access_token=self.invalid_token)

        with self.assertRaises(ExpireTokenException):
            introspector.introspect()
