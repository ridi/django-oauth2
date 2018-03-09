import typing

from ridi_oauth2.common.constants import HttpMethod, OAuth2GrantType
from ridi_oauth2.common.dtos import TokenData
from .base import BaseGrant


class RefreshTokenGrant(BaseGrant):
    GRANT_TYPE = OAuth2GrantType.REFRESH_TOKEN

    def get_authorization_url(self, *args, **kwargs) -> typing.Tuple[str, str]:
        raise NotImplementedError

    def get_access_token(self, refresh_token: str, *args, **kwargs) -> TokenData:  # flake8: noqa: W0221  # pylint:disable=arguments-differ
        data = {
            'grant_type': self.GRANT_TYPE,
            'refresh_Token': refresh_token,
            'client_id': self.client_info.client_id,
            'client_secret': self.client_info.client_secret,
        }

        if self.client_info.scope:
            data['scope'] = self.client_info.scope

        return TokenData.from_dict(self._request(
            method=HttpMethod.POST, url=self.auth_server_info.token_url, data=data, headers={'Accept': 'application/json', }
        ))
