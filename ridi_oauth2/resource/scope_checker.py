import typing

from ridi_oauth2.resource.constants import Scope

REQUIRE_SCOPE_TYPE = typing.TypeVar('REQUIRE_SCOPE_TYPE', typing.Tuple, typing.List, str)


class ScopeChecker:
    @classmethod
    def check(cls, require_scopes: typing.List[REQUIRE_SCOPE_TYPE], user_scopes: typing.List[str]) -> bool:
        if Scope.ALL in user_scopes:
            return True

        if not require_scopes:
            return True

        return cls._or(require_scopes=require_scopes, user_scopes=user_scopes)

    @classmethod
    def _or(cls, require_scopes: typing.List[REQUIRE_SCOPE_TYPE], user_scopes: typing.List[str]) -> bool:
        return any(cls._iterate_scopes(require_scopes=require_scopes, user_scopes=user_scopes))

    @staticmethod
    def _and(and_scopes: typing.Iterable, user_scopes: typing.List[str]) -> bool:
        for scope in and_scopes:
            if scope not in user_scopes:
                return False

        return True

    @classmethod
    def _iterate_scopes(cls, require_scopes: typing.List[REQUIRE_SCOPE_TYPE], user_scopes: typing.List[str]) -> typing.Iterable[bool]:
        for require_scope in require_scopes:
            if isinstance(require_scope, str):
                yield require_scope in user_scopes
            elif isinstance(require_scope, typing.Iterable):  # check isinstance tuple or list
                yield cls._and(and_scopes=require_scope, user_scopes=user_scopes)
            else:
                yield False
