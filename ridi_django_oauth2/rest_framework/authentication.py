from rest_framework.authentication import BaseAuthentication


class OAuth2Authentication(BaseAuthentication):

    def authenticate(self, request):
        user = getattr(request._request, 'user', None)

        if not user or not user.is_active:
            return None

        return user, None
