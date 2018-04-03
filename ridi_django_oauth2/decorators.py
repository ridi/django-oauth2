import typing

from django.http import HttpResponse, HttpResponseForbidden

from ridi_django_oauth2.response import HttpUnauthorizedResponse
from ridi_oauth2.resource.scope_checker import ScopeChecker

RESPONSE_HANDLER_TYPE = typing.Optional[typing.Callable]


def login_required(response_handler: RESPONSE_HANDLER_TYPE=None):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            user = request.user

            if not user or not user.is_authenticated:
                return _process_response_handler(request, response_handler, *args, **kwargs) or HttpUnauthorizedResponse()

            token_info = getattr(request.user, 'token_info', None)
            if token_info is None:
                return _process_response_handler(request, response_handler, *args, **kwargs) or HttpUnauthorizedResponse()

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def scope_required(required_scopes: typing.List, response_handler: RESPONSE_HANDLER_TYPE=None):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            token_info = request.user.token_info

            if not ScopeChecker.check(require_scopes=required_scopes, user_scopes=token_info.scope):
                return _process_response_handler(
                    request, response_handler, required_scopes=required_scopes, *args, **kwargs
                ) or HttpResponseForbidden()

            return func(self, request, *args, **kwargs)
        return login_required(response_handler)(wrapper)
    return decorator


def _process_response_handler(request, response_handler: RESPONSE_HANDLER_TYPE, *args, **kwargs) -> typing.Optional[HttpResponse]:
    if response_handler is None:
        return None

    return response_handler(request, *args, **kwargs)
