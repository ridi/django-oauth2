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
    'RIDI_ridi_oauth2_ID': 'dummy_client_id',
    'RIDI_ridi_oauth2_SECRET': 'dummy_client_secret',

    'RIDI_OAUTH2_AUTHORIZATION_URL': 'http://localhost/oauth2/authorize/',
    'RIDI_OAUTH2_TOKEN_URL': 'http://localhost/oauth2/token/',
    'RIDI_OAUTH2_INTERNAL_AUTH_ISS': 'library-admin',
    'RIDI_OAUTH2_INTERNAL_AUTH_AUD': 'account',
    'RIDI_OAUTH2_INTERNAL_AUTH_TTL_SECONDS': 100,
    'RIDI_OAUTH2_INTERNAL_AUTH_ALG': 'RS256',
    'RIDI_OAUTH2_INTERNAL_AUTH_URL': 'https://account.dev.ridi.io/oauth2/keys/public',
    'RIDI_OAUTH2_INTERNAL_AUTH_PRIVATE_KEY': '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEA1rL5PCEv2PaAASaGldzfnlo0MiMCglC+eFxYHgUfa6a7qJhj\no0QX8LeAelBlQpMCAMVGX33jUJ2FCCP/QDk3NIu74AgP7F3Z7IdmVvOfkt2myF1n\n3ZDyCHKdyi7MnOBtHIQCqQRGZ4XH2Ss5bmg/FuplBFT82e14UVmZx4kP+HwDjaSp\nvYHoTr3b5j20Ebx7aIy/SVrWeY0wxeAdFf+EOuEBQ+QIIe5Npd49gzq4CGHeNJlP\nQjs0EjMZFtPutCrIRSoEaLwccKQEIHcMSbsBLCJIJ5OuTmtK2WaSh7VYCrJsCbPh\n5tYKF6akN7TSOtDwGQVKwJjjOsxkPdYXNoAnIQIDAQABAoIBAGxaiORqz04NIY7z\nFYs+nHC7j4oaFyMTgv0Vhbco2LGoxR6SQf7c18Q5qBKSznfp32HqLdj1nKpLxR7V\no/WSqqTPPLMU/oxI1TnFH8YUT918FbcbRNcSVsQirDWkpskpjoeMrBcGvE10u+aD\nJQnufKChDPhBuBZ3/Xf4415Lcw7xAsooHWxN5dBlq80ITyO3Rpwp7VayNRg3fzqy\ndZgsZoutyJmKd5dyKpckCpnGXOI1uvs/bnL2GLWWZvAS7/PDm+8pv3iVzmLB4J4J\njogLtJteHczxvVpIEotTAI7hLyb89k1NRncGE7zxKwtP0sIp1qg7AZGlVE8YImSg\nBhA4uU0CgYEA4uLFIx3td6jWstFok6/J36VHM8K/o8BqWgHqlypfwBAGMTuXwNHY\nMwFQNyTsT0BHoFN8e60s5wE1PxlL+hrjepXWxyCyWoHJqHpi3wqdDTMLkwniQnYr\n4c9cKcOAbkbVo+zsycuXiEQvXzLiltYII4P3KyBH4T+kQJM+4j8drocCgYEA8j/e\nXEJZaAAN95wUhfw1yfuJhXvZ5sB//nJlxCEnY3Kr5/o36eRTDGYai9qEkZEi2Ntz\nlB57mZQdI+VSRU5OADmQUYTVY5f+KQenzA0HnEFT/8aBdEvvGAWQDnULS4UPLqZS\nDUqV4L/CuBXhlHE7vz7nbNfQGzu+WG6EdJBb/xcCgYBwXjOYotfbbal3wrLyghuP\nQkIzZn6XUVLa5RwUZg4qB0Wp2IPeIY/cIwhhZ04KKiHPS8nZTvlwJ28Bozu30N1c\n9xz6Xj03ChSf9o1FPfJueRuAZWLD29b77UEOBh9zfm2M1GipwMV53ZtAoOkMH1DE\nljUyDLjM3EIzIToBv5SpvQKBgFSniRcIgKHdUwQyYOGpj0p0QkyJSU5f+tp6M6Hk\nTBVunzBDuoJbrcHpdGFnDWipJVpO5gbe2CaFIeHHY4agpJVjiFFUcBWLqd/AsxyV\neRFbqvT484gmePkWCI9ky3uqlfGhYY8Pf2y41lzqGJh9MXnVi533lNvPducER/lL\n8TolAoGANsr7iMbS5+iM6PvbSnkoNecVB2uScUO8K0ZIMNc2NDq1C+7tOGCQSi93\nIk7xlStrOD7vhmSSZuvUMZ23F7R9b8RXq0XIfokKYkPiCUjdrgC9PP54CDwUbglS\nlKP4SrbeuaTbTuMuuN6es7h1kkcz5qORtm1hWXLFTmloqYe4r5Q=\n-----END RSA PRIVATE KEY-----',
    'RIDI_OAUTH2_INTERNAL_AUTH_CLIENT_ID': 'dummy_client'
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
