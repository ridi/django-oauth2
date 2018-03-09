import typing
from json import JSONDecodeError

import requests

from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.client.exceptions import AuthorizationException, OAuthFailureException
from ridi_oauth2.common.constants import HttpStatusCode
from ridi_oauth2.common.dtos import TokenData


class BaseGrant:
    GRANT_TYPE = None

    def __init__(
            self, client_info: ClientInfo, auth_server_info: AuthorizationServerInfo
    ):
        self.client_info = client_info
        self.auth_server_info = auth_server_info

    def get_authorization_url(self, *args, **kwargs) -> typing.Tuple[str, str]:
        raise NotImplementedError

    def get_access_token(self, *args, **kwargs) -> TokenData:
        raise NotImplementedError

    @classmethod
    def _request(cls, method: str, url: str, data: typing.Dict, headers: typing.Dict=None) -> typing.Dict:
        try:
            response = requests.request(method=method, url=url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except JSONDecodeError:
            raise AuthorizationException()
        except requests.HTTPError as e:
            cls._process_exception(exception=e)

    @staticmethod
    def _process_exception(exception: requests.HTTPError):
        response = exception.response

        if response.status_code != HttpStatusCode.HTTP_400_BAD_REQUEST:
            raise exception

        try:
            error_response = response.json()
        except JSONDecodeError:
            raise exception

        error = error_response.get('error', None)
        error_description = error_response.get('error_description', None)
        error_uri = error_response.get('error_uri', None)

        error_exception = OAuthFailureException(error_code=error, description=error_description, error_uri=error_uri)
        raise error_exception
