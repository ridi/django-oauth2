
from ridi_oauth2.client.dtos import AuthorizationServerInfo, ClientInfo
from ridi_oauth2.client.exceptions import NotSupportedGrantException
from ridi_oauth2.client.grant.authorization_code import AuthorizationCodeGrant
from ridi_oauth2.client.grant.base import BaseGrant
from ridi_oauth2.client.grant.refresh_token import RefreshTokenGrant
from ridi_oauth2.common.constants import OAuth2GrantType


class OAuth2GrantFactory:
    @staticmethod
    def get_grant(grant_type: str, client_info: ClientInfo, auth_server_info: AuthorizationServerInfo) -> BaseGrant:
        if grant_type == OAuth2GrantType.AUTHORIZATION_CODE:
            return AuthorizationCodeGrant(client_info=client_info, auth_server_info=auth_server_info)
        elif grant_type == OAuth2GrantType.REFRESH_TOKEN:
            return RefreshTokenGrant(client_info=client_info, auth_server_info=auth_server_info)

        raise NotSupportedGrantException()
