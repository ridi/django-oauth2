import base64
import hashlib
import hmac
import json
import string
import time
import unittest

import jwt

from ridi_oauth2.common.utils.string import generate_random_str


class JWTTestCase(unittest.TestCase):
    def setUp(self):
        self.secret = generate_random_str(chars=string.ascii_letters + string.digits + string.punctuation)
        self.claim = {
            "sub": "testuser",
            "u_idx": 1111,
            "exp": int(time.time()) + 300,
            "client_id": "asfeih29snv8as213i",
            "scope": "all"
        }
        self.alg = 'HS256'

    def test_jwt_encode(self):
        header = base64.urlsafe_b64encode(json.dumps({'typ': 'JWT', 'alg': self.alg}, separators=(',', ':')).encode('utf-8'))\
            .replace(b'=', b'')
        payload = base64.urlsafe_b64encode(json.dumps(self.claim, separators=(',', ':')).encode('utf-8')).replace(b'=', b'')
        signature = base64.urlsafe_b64encode(
            hmac.new(self.secret.encode('utf-8'), msg=b'.'.join([header, payload]), digestmod=hashlib.sha256).digest()
        ).replace(b'=', b'')

        _token_origin = '.'.join([header.decode(), payload.decode(), signature.decode()])
        _token = jwt.encode(self.claim, self.secret, algorithm=self.alg).decode()

        self.assertEqual(_token_origin, _token)

    def test_jwt_decode(self):
        _token = jwt.encode(self.claim, self.secret, algorithm=self.alg).decode()
        self.assertDictEqual(jwt.decode(_token, self.secret, algorithms=[self.alg]), self.claim)
