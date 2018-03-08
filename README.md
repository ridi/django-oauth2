
# Ridi-OAuth2-Client

## Introduction


## Description


## Requirement
- `Django 2.0.0` or higher
- `Python 3.6` or higher


## Usage

``` python

INSTALLED_APPS = [
    # ...
    'django_oauth2_client',
]

# Middleware Setting
MIDDLEWARE_CLASSES = (
    # ...
    'django_oauth2_client.middlewares.AuthenticationMiddleware',
)

AUTH_USER_MODEL = 'django_oauth2_client.RidiUser'


# RIDI Setting
RIDI_OAUTH2_JWT_SECRET = 'this-is-jwt-secret'
RIDI_OAUTH2_CLIENT_ID = 'this-is-client-id'
RIDI_OAUTH2_CLIENT_SECRET = 'this-is-client-secret'

RIDI_OAUTH2_AUTHORIZATION_URL = 'https://{auth_server_host}/oauth2/authorize/'
RIDI_OAUTH2_TOKEN_URL: 'https://{auth_server_host}/oauth2/token/'
```


## TODO

- Write Docs
- Travis CI
