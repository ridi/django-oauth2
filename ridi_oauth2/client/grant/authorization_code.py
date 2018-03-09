import typing
import urllib.parse

from ridi_oauth2.common.constants import HttpMethod, OAuth2GrantType
from ridi_oauth2.common.dtos import TokenData
from ridi_oauth2.common.utils.string import generate_random_str
from .base import BaseGrant


class AuthorizationCodeGrant(BaseGrant):
    GRANT_TYPE = OAuth2GrantType.AUTHORIZATION_CODE

    def get_authorization_url(self, *args, **kwargs) -> typing.Tuple[str, str]:
        state = generate_random_str()
        query = urllib.parse.urlencode({
            'client_id': self.client_info.client_id,
            'redirect_uri': self.client_info.redirect_uri,
            'scope': self.client_info.scope,
            'state': state,
            'response_type': 'code',
        })
        authorize_url = '{}?{}'.format(self.auth_server_info.authorization_url, query)
        return authorize_url, state

    def get_access_token(self, code: str, *args, **kwargs) -> TokenData:  # flake8: noqa: W0221  # pylint:disable=arguments-differ
        data = {
            'grant_type': self.GRANT_TYPE,
            'code': code,
            'redirect_uri': self.client_info.redirect_uri,
            'client_id': self.client_info.client_id,
            'client_secret': self.client_info.client_secret,
        }

        return TokenData.from_dict(self._request(
            method=HttpMethod.POST, url=self.auth_server_info.token_url, data=data, headers={'Accept': 'application/json', }
        ))
