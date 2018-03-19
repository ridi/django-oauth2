import typing
import urllib.parse
from json import JSONDecodeError

import requests

from ridi_oauth2.client.constants import OAuth2GrantType
from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo, TokenData
from ridi_oauth2.client.exceptions import InvalidResponseException, OAuthFailureException
from ridi_oauth2.common.constants import HttpMethod


class Grant:
    def __init__(
            self, client_info: ClientInfo, auth_server_info: AuthorizationServerInfo
    ):
        self.client_info = client_info
        self.auth_server_info = auth_server_info

    def authorize(self, state: str) -> str:
        query = urllib.parse.urlencode({
            'client_id': self.client_info.client_id,
            'redirect_uri': self.client_info.redirect_uri,
            'scope': self.client_info.scope,
            'state': state,
            'response_type': 'code',
        })
        authorize_url = '{}?{}'.format(self.auth_server_info.authorization_url, query)
        return authorize_url

    def code(self, code: str) -> TokenData:
        data = self._get_default_token_data(OAuth2GrantType.AUTHORIZATION_CODE)
        data['code'] = code
        data['redirect_uri'] = self.client_info.redirect_uri

        return self._request_token(data=data)

    def refresh(self, refresh_token: str) -> TokenData:
        data = self._get_default_token_data(OAuth2GrantType.REFRESH_TOKEN)
        data['refresh_token'] = refresh_token

        if self.client_info.scope:
            data['scope'] = self.client_info.scope

        return self._request_token(data=data)

    def _get_default_token_data(self, grant_type: str) -> typing.Dict:
        return {
            'grant_type': grant_type,
            'client_id': self.client_info.client_id,
            'client_secret': self.client_info.client_secret,
        }

    def _request_token(self, data: typing.Dict) -> TokenData:
        return self._request(
            method=HttpMethod.POST, url=self.auth_server_info.token_url, data=data, headers={'Accept': 'application/json', }
        )

    @classmethod
    def _request(cls, method: str, url: str, data: typing.Dict, headers: typing.Dict=None) -> TokenData:
        try:
            response = requests.request(method=method, url=url, data=data, headers=headers)
            response.raise_for_status()
            return TokenData.from_dict(response.json())
        except JSONDecodeError:
            raise InvalidResponseException()
        except requests.HTTPError as e:
            cls._process_exception(exception=e)

    @staticmethod
    def _process_exception(exception: requests.HTTPError):
        response = exception.response

        try:
            error_response = response.json()
        except JSONDecodeError:
            raise exception

        error = error_response.get('error', None)
        error_description = error_response.get('error_description', None)
        error_uri = error_response.get('error_uri', None)

        error_exception = OAuthFailureException(error_code=error, description=error_description, error_uri=error_uri)
        raise error_exception
