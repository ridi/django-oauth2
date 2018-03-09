import typing

from ridi_oauth2.resource.constants import DEFAULT_SCOPE_DELIMITER, Scope

USER_SCOPE_TYPE = typing.TypeVar('USER_SCOPE_TYPE', typing.List, str)


def scope_check(require_scopes: typing.List[str], user_scopes: USER_SCOPE_TYPE, delimiter: str=DEFAULT_SCOPE_DELIMITER) -> bool:
    user_scopes = _parse_user_scopes(user_scopes=user_scopes, delimiter=delimiter)

    if Scope.ALL in user_scopes:
        return True

    for scope in require_scopes:
        if scope not in user_scopes:
            return False

    return True


def _parse_user_scopes(user_scopes: USER_SCOPE_TYPE, delimiter: str=' ') -> typing.List:
    scopes = user_scopes
    if isinstance(scopes, str):
        scopes = scopes.split(delimiter)

    return scopes
