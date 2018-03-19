

class OAuth2GrantType:
    AUTHORIZATION_CODE = 'authorization_code'
    IMPLICIT = 'implicit'
    REOUSRCE_OWNER_PASSWORD_CREDENTIALS = 'resource_owner_password_credentials'
    CLIENT_CREDENTIALS = 'client_credentials'
    REFRESH_TOKEN = 'refresh_token'


class OAuth2ErrorCode:
    INVALID_REQUEST = 'invalid_request'
    INVALID_CLIENT = 'invalid_client'
    INVALID_GRANT = 'invalid_grant'
    UNAUTHORIZED_CLIENT = 'unauthorized_client'
    UNSUPPORTED_GRANT_TYPE = 'unsupported_grant_type'
    INVALID_SCOPE = 'invalid_scope'
