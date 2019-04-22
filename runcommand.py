import os
import sys

import django
from django.conf import settings

sys.path.append(os.path.abspath('./src'))


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
    'RIDI_OAUTH2_JWT_SECRETS': [
        {
            'kid': '0',
            'secret': 'dummy_jwt_secret',
            'alg': 'HS256'
        },
    ],
    'RIDI_ridi_oauth2_ID': 'dummy_client_id',
    'RIDI_ridi_oauth2_SECRET': 'dummy_client_secret',

    'RIDI_OAUTH2_AUTHORIZATION_URL': 'http://localhost/oauth2/authorize/',
    'RIDI_OAUTH2_TOKEN_URL': 'http://localhost/oauth2/token/',
}


def run_command(*args):
    settings.configure(**SETTINGS_DICT)
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(args)


if __name__ == '__main__':
    run_command(*sys.argv[:])
