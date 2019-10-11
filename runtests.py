import os
import sys

import django
from django.conf import settings
from django.contrib.auth import get_user_model

sys.path.append(os.path.abspath('./src'))


def _get_user_from_token_info(token_info):
    user, _ = get_user_model().objects.get_or_create(u_idx=token_info.u_idx)
    return user


SETTINGS_DICT = {
    'DEBUG': True,
    'USE_TZ': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    'AUTH_USER_MODEL': 'ridi_django_oauth2.RidiUser',
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'ridi_django_oauth2',
        'tests',
    ],
    'MIDDLEWARE_CLASSES': (
        'ridi_django_oauth2.middlewares.AuthenticationMiddleware',
    ),
    'RIDI_ridi_oauth2_ID': 'dummy_client_id',
    'RIDI_ridi_oauth2_SECRET': 'dummy_client_secret',

    'RIDI_OAUTH2_AUTHORIZATION_URL': 'http://localhost/oauth2/authorize/',
    'RIDI_OAUTH2_TOKEN_URL': 'http://localhost/oauth2/token/',
    'RIDI_OAUTH2_KEY_URL': 'https://account.dev.ridi.io/oauth2/keys/public',
    'RIDI_OAUTH2_GET_USER_FROM_TOKEN_INFO': _get_user_from_token_info
}


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    settings.configure(**SETTINGS_DICT)
    django.setup()

    # Run tests
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    test_runner = TestRunner()
    failures = test_runner.run_tests(test_args, interactive=False)

    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
