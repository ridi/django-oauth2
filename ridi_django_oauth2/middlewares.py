from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from ridi_django_oauth2.utils.token import get_token_from_cookie, get_token_info


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = AnonymousUser()

        token = get_token_from_cookie(request=request)
        token_info = None
        if token.access_token:
            token_info = get_token_info(token.access_token.token)

        if token_info is not None:
            user, _ = get_user_model().objects.get_or_create(u_idx=token_info.u_idx)
            user.token = token
            user.token_info = token_info
            request.user = user

        return None
