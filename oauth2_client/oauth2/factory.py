
from oauth2_client.constants import OAuth2GrantType
from oauth2_client.exceptions import NotSupportedGrantException
from oauth2_client.oauth2.dtos import AuthorizationServerInfo, ClientInfo
from oauth2_client.oauth2.grant.authorization_code import AuthorizationCodeGrant
from oauth2_client.oauth2.grant.base import BaseGrant
from oauth2_client.oauth2.grant.refresh_token import RefreshTokenGrant


class OAuth2GrantFactory:
    @staticmethod
    def get_grant(grant_type: str, client_info: ClientInfo, auth_server_info: AuthorizationServerInfo) -> BaseGrant:
        if grant_type == OAuth2GrantType.AUTHORIZATION_CODE:
            return AuthorizationCodeGrant(client_info=client_info, auth_server_info=auth_server_info)
        elif grant_type == OAuth2GrantType.REFRESH_TOKEN:
            return RefreshTokenGrant(client_info=client_info, auth_server_info=auth_server_info)

        raise NotSupportedGrantException
