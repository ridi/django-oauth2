# django-oauth2
[![Build Status](https://travis-ci.org/ridi/django-oauth2.svg?branch=master)](https://travis-ci.org/ridi/django-oauth2)

## Introduction
- OAuth2 Resource 서버를 구현하기 위한 Django용 라이브러리입니다.
    - 해당 라이브러리는 리디의 OAuth2 Resource 서버 규칙에 따라 작성 되었습니다.

## Requirement
- `Django 2.0.0` or higher
- `Python 3.6` or higher


## Usage

``` python
INSTALLED_APPS = [
    # ...
    'ridi_django_oauth2',
]

# Middleware Setting
MIDDLEWARE_CLASSES = (
    # ...
    'ridi_django_oauth2.middlewares.AuthenticationMiddleware',
)

AUTH_USER_MODEL = 'ridi_django_oauth2.RidiUser'


# RIDI Setting
RIDI_OAUTH2_JWT_SECRETS = [
    {
        'kid': '0',
        'secret': 'this-is-hs256-key',
        'alg': 'HS256',
    },
    {
        'kid': '1',
        'secret': 'this-is-rs256-public-key',
        'alg': 'RS256',
    },
]
RIDI_OAUTH2_CLIENT_ID = 'this-is-client-id'
RIDI_OAUTH2_CLIENT_SECRET = 'this-is-client-secret'

RIDI_OAUTH2_AUTHORIZATION_URL = 'https://{auth_server_host}/oauth2/authorize/'
RIDI_OAUTH2_TOKEN_URL: 'https://{auth_server_host}/oauth2/token/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ridi_django_oauth2.rest_framework.authentication.OAuth2Authentication',
    )
}
```


## TODO

- Write Docs
- MySQL Test
